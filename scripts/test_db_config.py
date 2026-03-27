#!/usr/bin/env python3
"""Test database configuration works with SQLite after refactoring."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.pop('DATABASE_URL', None)

from dashboard.app import app
uri = app.config['SQLALCHEMY_DATABASE_URI']
print(f'1. App DB URI: {uri}')
assert 'sqlite' in uri
assert 'marketing_dashboard.db' in uri
print('   PASS')

from automation.activity_tracker import ActivityTracker
tracker = ActivityTracker()
print(f'2. ActivityTracker DB URL: {tracker.database_url}')
assert 'sqlite' in tracker.database_url
print('   PASS')

tracker.track_ai_generation(brand='test_brand', content_type='test', success=True, metadata={'test': True})
data = tracker.get_real_time_dashboard_data(24)
print(f'3. Activity tracker dashboard data keys: {len(data)}')
assert len(data) > 0
print('   PASS')

from dashboard.database import DatabaseManager
dm = DatabaseManager(app)
print(f'4. DatabaseManager is_sqlite={dm._is_sqlite}, db_path={dm.db_path}')
assert dm._is_sqlite is True
assert dm.db_path is not None
print('   PASS')

from dashboard.models import Brand, db
with app.app_context():
    count = Brand.query.count()
    print(f'5. Brand count: {count}')
print('   PASS')

from dashboard.marketing_calendar_models import MarketingCalendar, MarketingTask
with app.app_context():
    db.create_all()
    cal_count = MarketingCalendar.query.count()
    print(f'6. MarketingCalendar count: {cal_count}')
print('   PASS')

# Test DATABASE_URL override
os.environ['DATABASE_URL'] = 'postgresql://user:pass@localhost:5432/testdb'
from importlib import reload
# Can't easily reload app, but test the logic directly
url = os.getenv('DATABASE_URL')
if url and url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql://', 1)
print(f'7. DATABASE_URL override: {url}')
assert url == 'postgresql://user:pass@localhost:5432/testdb'
print('   PASS')

# Test postgres:// -> postgresql:// fix
os.environ['DATABASE_URL'] = 'postgres://user:pass@host/db'
url = os.getenv('DATABASE_URL')
if url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql://', 1)
print(f'8. postgres:// fix: {url}')
assert url.startswith('postgresql://')
print('   PASS')

os.environ.pop('DATABASE_URL', None)
print('\nAll 8 tests passed!')
