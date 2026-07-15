#!/usr/bin/env python3
"""
One-time setup: create NullRecords brand in ForgeMarketing and copy email config.
Run from: /Users/greglind/Projects/NullRecords/ForgeMarketing/
"""
import sqlite3
from datetime import datetime

db = '/Users/greglind/Projects/NullRecords/ForgeMarketing/data/marketing_dashboard.db'
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
now = datetime.now().isoformat()

# 1. Create brand
existing = conn.execute('SELECT id FROM brands WHERE name="nullrecords"').fetchone()
if existing:
    brand_id = existing['id']
    print(f'NullRecords brand already exists (id={brand_id})')
else:
    conn.execute(
        'INSERT INTO brands (name, display_name, description, website_url, is_active, is_template, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)',
        ('nullrecords', 'NullRecords / My Evil Robot Army',
         'Independent music label — nu jazz, lofi, experimental electronic',
         'https://www.nullrecords.com', 1, 0, now, now)
    )
    brand_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    print(f'Created NullRecords brand (id={brand_id})')

# 2. Copy email config from brand 1
src = conn.execute('SELECT * FROM brand_email_configs WHERE brand_id=1').fetchone()
existing_cfg = conn.execute('SELECT id FROM brand_email_configs WHERE brand_id=?', (brand_id,)).fetchone()

if existing_cfg:
    print('Email config already exists for NullRecords brand')
elif src:
    src = dict(src)
    conn.execute(
        '''INSERT INTO brand_email_configs
           (brand_id, provider, api_key, api_token, smtp_host, smtp_port, smtp_user, smtp_password,
            from_email, from_name, reply_to_email, reply_to_name, is_primary, max_send_per_day,
            rate_limit_per_minute, is_verified, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (brand_id, src['provider'], src['api_key'] or '', src['api_token'],
         src['smtp_host'], src['smtp_port'], src['smtp_user'], src['smtp_password'],
         'team@nullrecords.com', 'NullRecords Music',
         'team@nullrecords.com', 'Greg Lind | NullRecords',
         1, src['max_send_per_day'] or 50,
         src['rate_limit_per_minute'] or 10, 1, now, now)
    )
    print(f"Created email config: from team@nullrecords.com via {src['provider']}")
else:
    print('WARNING: no source email config found on brand 1 — add email config manually in ForgeMarketing settings')

conn.commit()
conn.close()
print('Setup complete.')
