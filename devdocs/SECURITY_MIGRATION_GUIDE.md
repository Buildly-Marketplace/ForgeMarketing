# Security & Configuration Migration Guide

## ⚠️ CRITICAL: Removing Hardcoded Credentials

This guide helps you migrate from hardcoded credentials to secure database-backed configuration.

## 🔍 Identified Security Issues

### Files with Hardcoded Credentials (MUST FIX)

1. **`automation/websites/buildly/tweets.py`**
   - Line 7: Hardcoded Twitter bearer token
   - **Action**: Remove and migrate to database

2. **`automation/websites/buildly/the_real_tweet.py`**
   - Line 17: Hardcoded consumer_secret
   - **Action**: Remove and migrate to database

3. **`automation/analytics/multi_brand_analytics.py`**
   - Lines 33, 42, 51, 60, 69: Hardcoded Google Analytics API key
   - **Action**: Remove and use `config_loader.get_google_analytics_credentials()`

4. **`marketing/buildly_user_outreach.py`**
   - Lines 100-101: Hardcoded SMTP credentials (password visible)
   - **Action**: Remove and use `config_loader.get_brand_email_config()`

5. **`automation/websites/foundry/analytics_reporter.py`**
   - Lines 30-31: Hardcoded SMTP credentials
   - **Action**: Remove and use database config

## 🔧 Migration Steps

### Step 1: Initialize Database Schema

```bash
# Create database tables
python3 ops/init_database.py
```

### Step 2: Migrate Existing Credentials

```bash
# Run migration script
python3 ops/migrate_credentials.py
```

This will:
- Read credentials from environment variables
- Store them securely in database
- Create audit log entries

### Step 3: Update Code to Use ConfigLoader

Replace hardcoded credentials with secure database lookups:

#### Before (INSECURE):
```python
# ❌ NEVER DO THIS
bearer_token = '<your-twitter-bearer-token>'
```

#### After (SECURE):
```python
# ✅ DO THIS INSTEAD
from config.config_loader import config_loader

twitter_creds = config_loader.get_twitter_credentials('buildly')
bearer_token = twitter_creds.get('bearer_token', '')
```

### Step 4: Configure via Admin UI

1. Start server: `./ops/startup.sh start`
2. Access admin panel: `http://localhost:8002/admin`
3. Navigate to Configuration
4. Add/Update credentials for each brand:
   - Email providers
   - Twitter/X API
   - Google Analytics
   - YouTube API
   - Other integrations

### Step 5: Remove Environment Variables

After verifying database configuration works:

1. Remove credentials from `.env` file
2. Keep only non-sensitive config:
   ```bash
   FLASK_ENV=production
   OLLAMA_HOST=http://localhost:11434
   DATABASE_URL=sqlite:///instance/dashboard.db
   ```

### Step 6: Verify Security

```bash
# Check for remaining hardcoded secrets
grep -r "api_key\|token\|password" automation/ --include="*.py" | grep -v "config_loader"
grep -r "bearer_token" automation/ --include="*.py" | grep -v "config_loader"
```

## 📝 Code Update Examples

### Example 1: Twitter Integration

**File**: `automation/websites/buildly/tweets.py`

```python
# BEFORE (INSECURE)
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMrgrQEAAAAAbybRYuQ%2F...'
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json',
}

# AFTER (SECURE)
from config.config_loader import config_loader

def get_twitter_headers(brand_name='buildly'):
    creds = config_loader.get_twitter_credentials(brand_name)
    bearer_token = creds.get('bearer_token', '')
    
    if not bearer_token:
        raise ValueError(f"Twitter bearer token not configured for {brand_name}")
    
    return {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }

headers = get_twitter_headers()
```

### Example 2: Email Configuration

**File**: `marketing/buildly_user_outreach.py`

```python
# BEFORE (INSECURE)
self.smtp_server = 'smtp-relay.brevo.com'
self.smtp_port = 587
self.smtp_user = '<your-brevo-smtp-user>'
self.smtp_password = 'F9BCg30JqkyZmVWw'  # ❌ NEVER COMMIT PASSWORDS

# AFTER (SECURE)
from config.config_loader import config_loader

email_config = config_loader.get_brand_email_config('buildly')
if email_config:
    self.smtp_server = email_config.smtp_host
    self.smtp_port = email_config.smtp_port
    self.smtp_user = email_config.smtp_user
    self.smtp_password = email_config.smtp_password
else:
    raise ValueError("Email configuration not found for buildly")
```

### Example 3: Google Analytics

**File**: `automation/analytics/multi_brand_analytics.py`

```python
# BEFORE (INSECURE)
'ga_api_key': '<your-google-analytics-api-key>',  # ❌ HARDCODED

# AFTER (SECURE)
from config.config_loader import config_loader

def get_brand_analytics_config(brand_name):
    ga_creds = config_loader.get_google_analytics_credentials(brand_name)
    return {
        'ga_property_id': ga_creds.get('property_id', ''),
        'ga_api_key': ga_creds.get('api_key', ''),
        'ga_credentials_file': ga_creds.get('credentials_file', '')
    }
```

## 🔒 Security Best Practices

### 1. Never Commit Secrets
```bash
# Add to .gitignore
.env
*.key
*.pem
*_credentials.json
```

### 2. Use Database for All Credentials
- API keys
- OAuth tokens
- Passwords
- Connection strings
- Service URLs with auth

### 3. Enable Audit Logging
All credential access is logged in `api_credential_logs` table:
```sql
SELECT * FROM api_credential_logs 
WHERE action = 'accessed' 
ORDER BY created_at DESC;
```

### 4. Rotate Credentials Regularly
Via admin panel:
1. Configuration → API Credentials
2. Select service
3. Update credentials
4. Test connection
5. Save

### 5. Encrypt Sensitive Data
Mark credentials as secret in database:
```python
config_loader.set_system_config(
    key='secret_key',
    value='my-secret-value',
    is_secret=True  # Marks for encryption
)
```

## 🧪 Testing After Migration

### 1. Test Email Sending
```bash
python3 -c "
from config.config_loader import config_loader
email_config = config_loader.get_brand_email_config('buildly')
print('Email config loaded:', email_config.from_email if email_config else 'NOT FOUND')
"
```

### 2. Test API Credentials
```bash
python3 -c "
from config.config_loader import config_loader
twitter_creds = config_loader.get_twitter_credentials('buildly')
print('Twitter configured:', bool(twitter_creds.get('bearer_token')))
"
```

### 3. Run Full Tests
```bash
./ops/startup.sh setup
./ops/startup.sh start
# Test all features via UI
```

## 📊 Migration Checklist

- [ ] Database schema created (`init_database.py`)
- [ ] Credentials migrated (`migrate_credentials.py`)
- [ ] All Python files updated to use `config_loader`
- [ ] Hardcoded credentials removed from code
- [ ] `.env` file cleaned (only non-sensitive config)
- [ ] Admin UI configuration verified
- [ ] Email sending tested
- [ ] Social media posting tested
- [ ] Analytics integrations tested
- [ ] Audit logs reviewed
- [ ] `.gitignore` updated
- [ ] Documentation updated
- [ ] Team notified of changes

## 🆘 Troubleshooting

### Credentials Not Found
```python
# Check database
from dashboard.models import BrandAPICredential, SystemConfig
print(SystemConfig.query.all())
print(BrandAPICredential.query.all())
```

### Fallback to Environment Variables
If database lookup fails, system falls back to environment variables:
```python
import os
print(os.getenv('TWITTER_BEARER_TOKEN'))
```

### Clear Cache
```python
from config.config_loader import config_loader
config_loader.clear_cache()
```

## 📞 Support

For issues:
1. Check `ops/server.log` for errors
2. Review `api_credential_logs` table
3. Verify database connectivity
4. Check admin UI for configuration status

## 🎯 Next Steps

After migration:
1. Remove old credential files
2. Update deployment scripts
3. Update CI/CD pipelines
4. Train team on new workflow
5. Schedule credential rotation
6. Set up monitoring for failed API calls

---

**⚠️ IMPORTANT**: Do NOT commit this migration until all hardcoded credentials are removed from the codebase.
