"""
Marketing Calendar API endpoints for campaign and task management.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from dashboard.marketing_calendar_models import (
    MarketingCalendar, MarketingTask, ContentTemplate, MarketingWeekly,
    TaskStatus, TaskPriority, TaskType, PlatformType
)
from dashboard.models import Brand, db
import json

marketing_calendar_bp = Blueprint('marketing_calendar', __name__, url_prefix='/api/marketing')


# ============ CAMPAIGNS ============

@marketing_calendar_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Get all marketing campaigns, optionally filtered by brand"""
    brand = request.args.get('brand')
    
    query = MarketingCalendar.query
    if brand:
        query = query.filter_by(brand_name=brand)
    
    campaigns = query.all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'brand_name': c.brand_name,
            'campaign_name': c.campaign_name,
            'campaign_slug': c.campaign_slug,
            'description': c.description,
            'goal': c.goal,
            'target_metric': c.target_metric,
            'start_date': c.start_date.isoformat(),
            'end_date': c.end_date.isoformat(),
            'budget': c.budget,
            'status': c.status,
            'owner': c.owner,
            'task_count': len(c.tasks),
            'completed_tasks': sum(1 for t in c.tasks if t.status == TaskStatus.COMPLETED),
            'created_at': c.created_at.isoformat()
        } for c in campaigns]
    })


@marketing_calendar_bp.route('/campaigns', methods=['POST'])
def create_campaign():
    """Create a new marketing campaign"""
    data = request.get_json()
    
    # Validate required fields
    required = ['brand_name', 'campaign_name', 'start_date', 'end_date']
    if not all(field in data for field in required):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    # Verify brand exists
    brand = Brand.query.filter_by(name=data['brand_name']).first()
    if not brand:
        return jsonify({'success': False, 'error': 'Brand not found'}), 404
    
    try:
        campaign = MarketingCalendar(
            brand_name=data['brand_name'],
            campaign_name=data['campaign_name'],
            campaign_slug=data.get('campaign_slug', data['campaign_name'].lower().replace(' ', '-')),
            description=data.get('description'),
            goal=data.get('goal'),
            target_metric=data.get('target_metric'),
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            budget=data.get('budget', 0),
            currency=data.get('currency', 'USD'),
            status=data.get('status', 'draft'),
            owner=data.get('owner'),
            notes=data.get('notes'),
            metadata=data.get('metadata', {})
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Campaign "{campaign.campaign_name}" created successfully',
            'data': {'id': campaign.id, 'campaign_name': campaign.campaign_name}
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@marketing_calendar_bp.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get campaign details with all tasks"""
    campaign = MarketingCalendar.query.get(campaign_id)
    if not campaign:
        return jsonify({'success': False, 'error': 'Campaign not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': campaign.id,
            'brand_name': campaign.brand_name,
            'campaign_name': campaign.campaign_name,
            'description': campaign.description,
            'goal': campaign.goal,
            'start_date': campaign.start_date.isoformat(),
            'end_date': campaign.end_date.isoformat(),
            'budget': campaign.budget,
            'status': campaign.status,
            'owner': campaign.owner,
            'tasks': [{
                'id': t.id,
                'task_name': t.task_name,
                'platform': t.platform.value,
                'status': t.status.value,
                'scheduled_date': t.scheduled_date.isoformat(),
                'priority': t.priority.value,
                'assigned_to': t.assigned_to,
                'is_automated': t.is_automated
            } for t in campaign.tasks],
            'created_at': campaign.created_at.isoformat()
        }
    })


# ============ TASKS ============

@marketing_calendar_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get marketing tasks with filtering"""
    brand = request.args.get('brand')
    status = request.args.get('status')
    platform = request.args.get('platform')
    assigned_to = request.args.get('assigned_to')
    calendar_id = request.args.get('calendar_id')
    
    query = MarketingTask.query
    
    if brand:
        query = query.filter_by(brand_name=brand)
    if status:
        query = query.filter_by(status=TaskStatus[status.upper()])
    if platform:
        query = query.filter_by(platform=PlatformType[platform.upper()])
    if assigned_to:
        query = query.filter_by(assigned_to=assigned_to)
    if calendar_id:
        query = query.filter_by(calendar_id=int(calendar_id))
    
    tasks = query.order_by(MarketingTask.scheduled_date).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': t.id,
            'task_name': t.task_name,
            'platform': t.platform.value,
            'status': t.status.value,
            'priority': t.priority.value,
            'scheduled_date': t.scheduled_date.isoformat(),
            'title': t.title,
            'assigned_to': t.assigned_to,
            'is_automated': t.is_automated,
            'calendar_id': t.calendar_id
        } for t in tasks]
    })


@marketing_calendar_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new marketing task"""
    data = request.get_json()
    
    required = ['brand_name', 'calendar_id', 'task_name', 'platform', 'scheduled_date']
    if not all(field in data for field in required):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        task = MarketingTask(
            calendar_id=data['calendar_id'],
            brand_name=data['brand_name'],
            task_name=data['task_name'],
            task_slug=data.get('task_slug', data['task_name'].lower().replace(' ', '-')),
            description=data.get('description'),
            task_type=TaskType[data.get('task_type', 'SOCIAL_POST').upper()],
            platform=PlatformType[data['platform'].upper()],
            scheduled_date=datetime.fromisoformat(data['scheduled_date']),
            scheduled_time=data.get('scheduled_time'),
            duration_minutes=data.get('duration_minutes'),
            assigned_to=data.get('assigned_to'),
            status=TaskStatus[data.get('status', 'DRAFT').upper()],
            priority=TaskPriority[data.get('priority', 'MEDIUM').upper()],
            is_automated=data.get('is_automated', False),
            title=data.get('title'),
            body=data.get('body'),
            metadata=data.get('metadata', {})
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Task "{task.task_name}" created successfully',
            'data': {'id': task.id, 'task_name': task.task_name}
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@marketing_calendar_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get task details"""
    task = MarketingTask.query.get(task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': task.id,
            'task_name': task.task_name,
            'description': task.description,
            'platform': task.platform.value,
            'task_type': task.task_type.value,
            'status': task.status.value,
            'priority': task.priority.value,
            'scheduled_date': task.scheduled_date.isoformat(),
            'title': task.title,
            'body': task.body,
            'assigned_to': task.assigned_to,
            'is_automated': task.is_automated,
            'metrics': task.performance_metrics,
            'created_at': task.created_at.isoformat()
        }
    })


@marketing_calendar_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = MarketingTask.query.get(task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    if 'status' in data:
        task.status = TaskStatus[data['status'].upper()]
    if 'priority' in data:
        task.priority = TaskPriority[data['priority'].upper()]
    if 'assigned_to' in data:
        task.assigned_to = data['assigned_to']
    if 'title' in data:
        task.title = data['title']
    if 'body' in data:
        task.body = data['body']
    if 'scheduled_date' in data:
        task.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
    if 'metrics' in data:
        task.performance_metrics = data['metrics']
    
    task.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Task "{task.task_name}" updated successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@marketing_calendar_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark a task as completed"""
    task = MarketingTask.query.get(task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    data = request.get_json() or {}
    
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.utcnow()
    task.executed_by = data.get('executed_by', 'system')
    task.execution_log = data.get('execution_log')
    task.performance_metrics = data.get('metrics', {})
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Task "{task.task_name}" marked as completed'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ CONTENT TEMPLATES ============

@marketing_calendar_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get content templates"""
    brand = request.args.get('brand')
    platform = request.args.get('platform')
    category = request.args.get('category')
    
    query = ContentTemplate.query
    
    if brand:
        query = query.filter_by(brand_name=brand)
    if platform:
        query = query.filter_by(platform=PlatformType[platform.upper()])
    if category:
        query = query.filter_by(category=category)
    
    templates = query.all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': t.id,
            'template_name': t.template_name,
            'platform': t.platform.value,
            'task_type': t.task_type.value,
            'category': t.category,
            'title_template': t.title_template,
            'usage_count': t.usage_count,
            'description': t.description
        } for t in templates]
    })


@marketing_calendar_bp.route('/templates', methods=['POST'])
def create_template():
    """Create a content template"""
    data = request.get_json()
    
    required = ['brand_name', 'template_name', 'platform', 'task_type']
    if not all(field in data for field in required):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        template = ContentTemplate(
            brand_name=data['brand_name'],
            template_name=data['template_name'],
            template_slug=data.get('template_slug', data['template_name'].lower().replace(' ', '-')),
            category=data.get('category'),
            platform=PlatformType[data['platform'].upper()],
            task_type=TaskType[data['task_type'].upper()],
            title_template=data.get('title_template'),
            body_template=data.get('body_template'),
            cta=data.get('cta'),
            hashtags=data.get('hashtags'),
            variables=data.get('variables', {}),
            description=data.get('description')
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Template "{template.template_name}" created',
            'data': {'id': template.id}
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ WEEKLY REPORTS ============

@marketing_calendar_bp.route('/weekly-reports', methods=['GET'])
def get_weekly_reports():
    """Get weekly marketing reports"""
    brand = request.args.get('brand')
    calendar_id = request.args.get('calendar_id')
    
    query = MarketingWeekly.query
    
    if brand:
        query = query.filter_by(brand_name=brand)
    if calendar_id:
        query = query.filter_by(calendar_id=int(calendar_id))
    
    reports = query.order_by(MarketingWeekly.week_start.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': r.id,
            'brand_name': r.brand_name,
            'week_start': r.week_start.isoformat(),
            'week_end': r.week_end.isoformat(),
            'posts_published': r.posts_published,
            'total_reach': r.total_reach,
            'total_engagement': r.total_engagement,
            'total_conversions': r.total_conversions,
            'signups': r.signups,
            'insights': r.insights
        } for r in reports]
    })


@marketing_calendar_bp.route('/weekly-reports', methods=['POST'])
def create_weekly_report():
    """Create a weekly marketing report"""
    data = request.get_json()
    
    required = ['brand_name', 'week_start', 'week_end']
    if not all(field in data for field in required):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    try:
        report = MarketingWeekly(
            brand_name=data['brand_name'],
            calendar_id=data.get('calendar_id'),
            week_start=datetime.fromisoformat(data['week_start']),
            week_end=datetime.fromisoformat(data['week_end']),
            posts_published=data.get('posts_published', 0),
            total_reach=data.get('total_reach', 0),
            total_engagement=data.get('total_engagement', 0),
            total_clicks=data.get('total_clicks', 0),
            total_conversions=data.get('total_conversions', 0),
            signups=data.get('signups', 0),
            platform_metrics=data.get('platform_metrics', {}),
            notes=data.get('notes'),
            insights=data.get('insights')
        )
        
        db.session.add(report)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Weekly report created',
            'data': {'id': report.id}
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ CALENDAR VIEW ============

@marketing_calendar_bp.route('/calendar-view', methods=['GET'])
def get_calendar_view():
    """Get tasks for calendar view (grouped by date)"""
    brand = request.args.get('brand')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = MarketingTask.query
    
    if brand:
        query = query.filter_by(brand_name=brand)
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        query = query.filter(MarketingTask.scheduled_date >= start)
    
    if end_date:
        end = datetime.fromisoformat(end_date)
        query = query.filter(MarketingTask.scheduled_date <= end)
    
    tasks = query.order_by(MarketingTask.scheduled_date).all()
    
    # Group by date
    calendar_data = {}
    for task in tasks:
        date_key = task.scheduled_date.date().isoformat()
        if date_key not in calendar_data:
            calendar_data[date_key] = []
        
        calendar_data[date_key].append({
            'id': task.id,
            'task_name': task.task_name,
            'platform': task.platform.value,
            'status': task.status.value,
            'priority': task.priority.value,
            'assigned_to': task.assigned_to,
            'is_automated': task.is_automated
        })
    
    return jsonify({
        'success': True,
        'data': calendar_data
    })
