---
title: Brand Management System Migration Guide
date: 2025-12-04
author: GitHub Copilot
category: Architecture
---

# Brand Management System Migration Guide

## Overview

This guide explains the transition from hardcoded brand references to a database-driven brand management system. This change enables:

- **Dynamic brand configuration** - Add/remove brands without code changes
- **Multi-tenant support** - Each brand has independent configuration
- **Centralized management** - All brand data managed via admin UI
- **Better security** - Credentials stored securely in database
- **Easier maintenance** - No need to update multiple files when adding brands

## Architecture Changes

### Before: Hardcoded Brands

```python
# ❌ OLD - Hardcoded brand list
brands = ['buildly', 'foundry', 'openbuild', 'radical', 'oregonsoftware']

# ❌ OLD - Hardcoded brand configuration  
BRAND_CONFIG = {
    'buildly': {
        'name': 'Buildly',
        'website': 'https://buildly.io',
        'email': 'team@buildly.io'
    },
    'foundry': {
        'name': 'Foundry',
        'website': 'https://firstcityfoundry.com',
        'email': 'team@firstcityfoundry.com'
    }
}
```

### After: Database-Driven

```python
# ✅ NEW - Load brands from database
from config.brand_loader import get_all_brands, get_brand_details

# Get all active brands
brands = get_all_brands()  # Returns ['buildly', 'foundry', 'openbuild', ...]

# Get brand configuration
brand_data = get_brand_details('buildly')
# Returns: {'name': 'buildly', 'display_name': 'Buildly', 'website_url': '...', ...}
```

## Database Schema

### Brand Model

```python
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)  # 'buildly', 'foundry', etc.
    display_name = db.Column(db.String(255))        # 'Buildly', 'Foundry', etc.
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(500))
    website_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    is_template = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
```

### Relationships

- **BrandEmailConfig**: Email provider credentials per brand
- **BrandAPICredential**: API credentials for services (Twitter, GA, YouTube)
- **BrandSettings**: Brand-specific settings and preferences

## Migration Process

### Step 1: Initialize Database

```bash
# Create database tables and load default brands
python3 ops/init_database.py
```

This creates 5 default brands:
- **buildly** - Buildly platform
- **foundry** - Foundry accelerator
- **openbuild** - OpenBuild community
- **radical** - Radical Therapy platform
- **oregonsoftware** - Oregon Software services

### Step 2: Update Code to Use Brand Loader

#### Simple Brand List

```python
# Before
brands = ['buildly', 'foundry', 'openbuild']

# After
from config.brand_loader import get_all_brands
brands = get_all_brands(active_only=True)
```

#### Brand Configuration

```python
# Before
if brand == 'buildly':
    website = 'https://buildly.io'
    email = 'team@buildly.io'

# After
from config.brand_loader import get_brand_details
brand_data = get_brand_details(brand)
website = brand_data['website_url']
email = brand_data['email']  # From BrandEmailConfig
```

#### Brand-Specific Logic

```python
# Before
BRAND_CONFIGS = {
    'buildly': {'setting1': 'value1'},
    'foundry': {'setting1': 'value2'}
}

# After
from config.brand_loader import BrandLoader
loader = BrandLoader()
brand_config = loader.get_brand_config(brand, config_type='settings')
```

### Step 3: Verify Changes

```bash
# Run brand audit tool
python3 ops/brand_audit.py

# Should show 0 HIGH priority issues
```

## Brand Loader API Reference

### Functions

#### `get_all_brands(active_only=True) -> List[str]`

Returns list of all brand names.

```python
from config.brand_loader import get_all_brands

# Get all active brands
brands = get_all_brands()
# Returns: ['buildly', 'foundry', 'openbuild', 'radical', 'oregonsoftware']

# Get all brands including inactive
all_brands = get_all_brands(active_only=False)
```

#### `get_brand_details(brand_name: str) -> Dict`

Returns full brand details.

```python
from config.brand_loader import get_brand_details

brand = get_brand_details('buildly')
# Returns: {
#     'id': 1,
#     'name': 'buildly',
#     'display_name': 'Buildly',
#     'description': 'Project management platform',
#     'website_url': 'https://buildly.io',
#     'is_active': True,
#     ...
# }
```

#### `get_brand_loader() -> BrandLoader`

Returns singleton BrandLoader instance.

```python
from config.brand_loader import get_brand_loader

loader = get_brand_loader()
brands = loader.get_all_brands()
config = loader.get_brand_config('buildly', config_type='email')
```

### BrandLoader Class Methods

#### `get_all_brands(active_only=True, include_details=False)`

```python
loader = BrandLoader()

# Get brand names
names = loader.get_all_brands()

# Get full brand objects
brands = loader.get_all_brands(include_details=True)
```

#### `get_brand_by_name(brand_name: str)`

```python
brand = loader.get_brand_by_name('buildly')
```

#### `get_brand_config(brand_name: str, config_type='all')`

```python
# Get all configuration
all_config = loader.get_brand_config('buildly', config_type='all')

# Get just email config
email_config = loader.get_brand_config('buildly', config_type='email')

# Get just API services
api_config = loader.get_brand_config('buildly', config_type='api')

# Get just settings
settings = loader.get_brand_config('buildly', config_type='settings')
```

#### `is_brand_active(brand_name: str)`

```python
if loader.is_brand_active('buildly'):
    # Process brand
    pass
```

#### `get_brand_mapping()`

```python
# Get name -> display_name mapping
mapping = loader.get_brand_mapping()
# Returns: {'buildly': 'Buildly', 'foundry': 'Foundry', ...}
```

## Common Migration Patterns

### Pattern 1: Iterating Over Brands

```python
# Before
for brand in ['buildly', 'foundry', 'openbuild']:
    process_brand(brand)

# After
from config.brand_loader import get_all_brands

for brand in get_all_brands():
    process_brand(brand)
```

### Pattern 2: Brand-Specific Configuration

```python
# Before
BRAND_SETTINGS = {
    'buildly': {'api_url': 'https://api.buildly.io'},
    'foundry': {'api_url': 'https://api.foundry.com'}
}
setting = BRAND_SETTINGS[brand]['api_url']

# After
from config.brand_loader import get_brand_details

brand_data = get_brand_details(brand)
setting = brand_data['website_url']  # or custom field
```

### Pattern 3: Conditional Brand Logic

```python
# Before
if brand == 'buildly':
    config = BUILDLY_CONFIG
elif brand == 'foundry':
    config = FOUNDRY_CONFIG

# After
from config.brand_loader import BrandLoader

loader = BrandLoader()
config = loader.get_brand_config(brand)
```

### Pattern 4: Fallback for Missing Brands

```python
from config.brand_loader import get_brand_details

brand_data = get_brand_details(brand)
if not brand_data:
    # Brand not found - use default
    brand_data = get_brand_details('buildly')
```

## Admin UI Management

### Adding a New Brand

1. Navigate to `/admin` in the dashboard
2. Click "Add Brand"
3. Fill in brand details:
   - Name (lowercase, no spaces): `newbrand`
   - Display Name: `New Brand`
   - Description: Brand description
   - Website URL: `https://newbrand.com`
   - Logo URL (optional)
4. Click "Save"
5. Configure email and API credentials in brand settings

### Updating Brand Configuration

1. Go to `/admin/brands`
2. Click brand name to edit
3. Update fields
4. Click "Save"

### Deactivating a Brand

1. Go to `/admin/brands`
2. Click brand name
3. Uncheck "Is Active"
4. Click "Save"

**Note**: Deactivated brands won't appear in `get_all_brands(active_only=True)`

## Audit and Validation

### Brand Audit Tool

Scans codebase for remaining hardcoded brand references:

```bash
python3 ops/brand_audit.py
```

Output shows:
- **HIGH priority**: Hardcoded brand lists that should use `get_all_brands()`
- **MEDIUM priority**: Brand-specific configuration dictionaries
- **LOW priority**: Default values and examples (may be acceptable)

### Example Output

```
⚠️  Found 120 hardcoded brand reference(s):

================================================================================
HIGH PRIORITY (45 issues)
================================================================================

📄 automation/analytics/analytics_manager.py
   Line   32: self.brands = ['buildly', 'foundry', 'openbuild', 'radical']
              → Use: from config.brand_loader import get_all_brands
                     brands = get_all_brands()
```

### Integration Testing

Test brand loading in your code:

```python
from config.brand_loader import get_all_brands, get_brand_details

# Test brand loading
brands = get_all_brands()
assert len(brands) >= 5, "Expected at least 5 brands"
assert 'buildly' in brands, "Buildly brand should exist"

# Test brand details
buildly = get_brand_details('buildly')
assert buildly is not None, "Buildly should have details"
assert buildly['is_active'] == True, "Buildly should be active"
```

## Fallback Behavior

If database is unavailable, `brand_loader` provides sensible fallbacks:

```python
def _get_default_brands() -> List[str]:
    """Fallback brands when database unavailable"""
    return ['buildly', 'foundry', 'openbuild', 'radical', 'oregonsoftware']
```

This ensures code works even if:
- Database connection fails
- Flask app not initialized
- Running in test/development mode

## Best Practices

### ✅ DO

- **Use `get_all_brands()`** for any brand iteration
- **Use `get_brand_details()`** for brand-specific configuration
- **Check brand is active** with `is_brand_active()` before processing
- **Handle None results** when brand not found
- **Use fallbacks** for optional configuration

### ❌ DON'T

- **Don't hardcode brand lists** - Always load from database
- **Don't hardcode brand config** - Use database/brand_loader
- **Don't assume brand exists** - Check return values
- **Don't modify brand data in code** - Use admin UI
- **Don't bypass brand_loader** - Centralize all brand access

## Troubleshooting

### Issue: Brand not found

```python
brand_data = get_brand_details('mybrand')
if not brand_data:
    print("Brand not in database - add via admin UI")
```

### Issue: Empty brand list

```python
brands = get_all_brands()
if not brands:
    # Database not initialized or all brands inactive
    print("Run: python3 ops/init_database.py")
```

### Issue: Circular import

```python
# If brand_loader creates circular import, use late import:
def my_function():
    from config.brand_loader import get_all_brands
    brands = get_all_brands()
```

### Issue: Flask app not found

Brand loader automatically creates Flask app context if needed. If this fails, pass app explicitly:

```python
from config.brand_loader import BrandLoader
from dashboard.app import create_app

app = create_app()
loader = BrandLoader(app)
brands = loader.get_all_brands()
```

## Migration Checklist

- [ ] Run `python3 ops/init_database.py` to create brands table
- [ ] Update code to use `get_all_brands()` instead of hardcoded lists
- [ ] Replace brand configuration dictionaries with `get_brand_details()`
- [ ] Run `python3 ops/brand_audit.py` to find remaining issues
- [ ] Test all brand-dependent functionality
- [ ] Configure brand credentials via admin UI
- [ ] Update deployment scripts to initialize database
- [ ] Update documentation with new brand management process

## Related Documentation

- **Database Architecture**: `devdocs/01_DATABASE_ARCHITECTURE.md`
- **Security Migration**: `devdocs/SECURITY_MIGRATION_GUIDE.md`
- **Admin Panel API**: `devdocs/03_ADMIN_PANEL_API.md`
- **Brand Audit Tool**: `ops/brand_audit.py`
- **Example Usage**: `examples/config_usage_examples.py`

## Summary

The brand management system migration enables:

1. **Dynamic brand management** - Add/remove brands without code changes
2. **Centralized configuration** - All brand data in one place
3. **Better security** - Credentials in database, not code
4. **Easier maintenance** - Update one source of truth
5. **Multi-tenant ready** - Each brand independently configured

**Key API**: `from config.brand_loader import get_all_brands, get_brand_details`

**Tools**: `ops/brand_audit.py` - Find hardcoded brand references

**Admin UI**: `/admin/brands` - Manage brands via web interface

For questions or issues, refer to related documentation or run the audit tool to identify remaining hardcoded references.
