"""Persistent, user-visible execution tracking for dashboard operations."""

from __future__ import annotations

from datetime import datetime
import json
import logging
from threading import Thread
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from dashboard.models import DashboardTask, DashboardTaskEvent, db

logger = logging.getLogger(__name__)

TaskReporter = Callable[[int, str, Optional[Dict[str, Any]]], None]
TaskRunner = Callable[[TaskReporter], Optional[Dict[str, Any]]]


def _add_event(task: DashboardTask, message: str, progress: Optional[int], level: str = 'info') -> None:
    db.session.add(DashboardTaskEvent(
        task_id=task.id,
        message=message,
        progress=progress,
        level=level,
    ))


def start_background_task(app, *, title: str, task_type: str, runner: TaskRunner,
                          brand_name: Optional[str] = None) -> DashboardTask:
    """Persist a queued task and execute it in a daemon thread with app context."""
    task = DashboardTask(
        id=str(uuid4()), title=title, task_type=task_type, brand_name=brand_name,
        status='queued', progress=0, message='Queued',
    )
    db.session.add(task)
    _add_event(task, 'Queued', 0)
    db.session.commit()
    task_id = task.id

    def execute() -> None:
        with app.app_context():
            current = DashboardTask.query.get(task_id)
            if current is None:
                return
            current.status = 'running'
            current.started_at = datetime.utcnow()
            current.message = 'Starting'
            _add_event(current, 'Started', 0)
            db.session.commit()

            def report(progress: int, message: str, detail: Optional[Dict[str, Any]] = None) -> None:
                current_task = DashboardTask.query.get(task_id)
                if current_task is None:
                    return
                bounded_progress = max(0, min(99, int(progress)))
                current_task.progress = bounded_progress
                current_task.message = message
                if detail is not None:
                    current_task.result = json.dumps(detail, default=str)
                _add_event(current_task, message, bounded_progress)
                db.session.commit()

            try:
                result = runner(report) or {}
                current = DashboardTask.query.get(task_id)
                current.status = 'succeeded'
                current.progress = 100
                current.message = result.get('message', 'Completed') if isinstance(result, dict) else 'Completed'
                current.result = json.dumps(result, default=str)
                current.finished_at = datetime.utcnow()
                _add_event(current, current.message, 100)
                db.session.commit()
            except Exception as exc:  # surfaced in the task center, never hidden behind a generic alert
                logger.exception('Dashboard task %s failed', task_id)
                db.session.rollback()
                current = DashboardTask.query.get(task_id)
                if current is not None:
                    current.status = 'failed'
                    current.message = 'Failed'
                    current.error_message = str(exc)
                    current.finished_at = datetime.utcnow()
                    _add_event(current, str(exc), current.progress, 'error')
                    db.session.commit()

    Thread(target=execute, name=f'dashboard-task-{task_id[:8]}', daemon=True).start()
    return task
