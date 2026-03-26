# tests/ Directory - Testing & Utilities

All test scripts, diagnostic utilities, and development utilities for ForgeMark.

## Quick Start

### Run Smoke Tests (No dependencies)
```bash
python tests/smoke_check.py
```

This validates:
- Environment setup
- Required files
- Configuration
- Deployment readiness

## Test Categories

### Smoke & Config Tests
- `smoke_check.py` - ⭐ Main smoke test runner (no pytest needed)
- `smoke/test_health.py` - API health endpoint checks
- `smoke/test_config.py` - Configuration file validation
- `crud/test_campaigns.py` - Campaign CRUD operations

### Multi-Tenant Architecture Tests
- `test_multitenancy_validation.py` - ⭐ Complete multi-tenant system validation (6 comprehensive tests)
  - Database initialization
  - Brand data and relationships
  - Real data enforcement
  - Audit logging
  - API structure
  - Model relationships

### Integration Tests
- `test_google_ads_connection.py`
- `test_crm_sync.py`
- `test_bluesky_connection.py`
- `test_social_automation.py`
- `test_discovery_complete.py`
- `test_campaign.py`
- `test_multi_account.py`
- `test_new_platforms.py`
- `test_service_account_connection.py`
- `test_analytics.html`

### Debug & Diagnostic
- `debug_brands.py` - Debug brand configuration
- `debug_crm_sync.py` - Debug CRM sync issues
- `diagnose_brevo_delivery.py` - Email delivery diagnostics
- `mailersend_diagnostic.py` - Brevo/Sendinblue diagnostics
- `mailersend_solutions.py` - Email solutions

### Setup & Configuration (One-time)
- `setup_automation_complete.py` - Full system setup
- `setup_automation.py` - Basic automation setup
- `setup_inactive_brands.py` - Configure inactive brands
- `setup_mastodon.py` - Mastodon setup
- `setup_service_account_auth.py` - Service account auth

### Utilities & Helpers
- `generate_posts.py` - Generate social posts
- `generate_recent_activity.py` - Generate activity feeds
- `email_delivery_final_report.py` - Email delivery report
- `email_stats_service.py` - Email statistics
- `email_verification_alternatives.py` - Email verification
- `email_templates.py` - Email template utilities
- `check_contact_data.py` - Validate contact data
- `complete_crm_sync.py` - CRM synchronization
- `create_email_demos.py` - Create email demos
- `activate_brands_api.py` - Activate brand APIs
- `add_unified_targets.py` - Add targets
- `show_crm_links.py` - Display CRM links
- `verify_email_delivery.py` - Verify delivery
- `quick_email_test.py` - Quick email test
- `branded_email_demo.py` - Brand email demo
- `google_ads_oauth_helper.py` - Google Ads OAuth helper
- `google_ads_setup_helper.py` - Google Ads setup
- `update_google_ads_config.py` - Update Google Ads config
- `update_service_account_config.py` - Update service account
- `unified_email_service.py` - Email service
- `unified_email_service_broken.py` - Broken email service (reference)

## Running Tests with pytest

```bash
# Install pytest
pip install pytest

# Run smoke tests
pytest tests/smoke/ -v

# Run CRUD tests
pytest tests/crud/ -v

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Common Commands

```bash
# Check system readiness
python tests/smoke_check.py

# Debug brand config
python tests/debug_brands.py

# Generate content
python tests/generate_posts.py

# Check contacts
python tests/check_contact_data.py

# Test Google Ads
python tests/test_google_ads_connection.py

# Test CRM sync
python tests/test_crm_sync.py
```

## Usage

Most files are runnable directly:
```bash
python tests/<script_name>.py
```

See individual script headers for specific usage and requirements.
