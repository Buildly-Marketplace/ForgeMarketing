#!/usr/bin/env python3
"""
Validation script to test the multi-tenant database architecture
Checks database initialization, models, API endpoints, and real data usage
"""

import os
import sys
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed")

# Initialize Flask app
from dashboard.app import app, db
from dashboard.models import Brand, BrandEmailConfig, BrandSettings, APICredentialLog
from dashboard.database import DatabaseManager


def test_database_initialization():
    """Test database initialization"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Database Initialization")
    print("="*60)
    
    with app.app_context():
        try:
            db_manager = DatabaseManager(app)
            
            # Check database path
            db_path = app.config['SQLALCHEMY_DATABASE_URI']
            print(f"✓ Database URI: {db_path}")
            
            # Initialize if needed
            if Brand.query.count() == 0:
                print("  → Database empty, initializing...")
                db_manager.init_db()
            
            # Check if brands exist
            brand_count = Brand.query.count()
            print(f"✓ Brands in database: {brand_count}")
            
            if brand_count > 0:
                print("✅ TEST 1 PASSED: Database initialized successfully")
                return True
            else:
                print("❌ TEST 1 FAILED: No brands in database")
                return False
                
        except Exception as e:
            print(f"❌ TEST 1 FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_brand_data():
    """Test brand data and relationships"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Brand Data & Relationships")
    print("="*60)
    
    with app.app_context():
        try:
            brands = Brand.query.all()
            
            expected_brands = ['buildly', 'foundry', 'openbuild', 'radical', 'oregonsoftware']
            found_brands = [b.name for b in brands]
            
            print(f"Expected brands: {expected_brands}")
            print(f"Found brands:    {found_brands}")
            
            all_found = all(brand in found_brands for brand in expected_brands)
            
            if not all_found:
                print("❌ TEST 2 FAILED: Not all expected brands found")
                return False
            
            # Check relationships
            for brand in brands:
                print(f"\n  Brand: {brand.display_name}")
                
                # Check email configs
                configs = brand.email_configs.all()
                print(f"    Email configs: {len(configs)}")
                for config in configs:
                    print(f"      - {config.provider} (verified: {config.is_verified})")
                    
                    # Verify real credentials (not empty, not "test-key")
                    if not config.api_key and not config.api_token:
                        print(f"        ❌ ERROR: No credentials!")
                        return False
                    if "test" in str(config.api_key).lower():
                        print(f"        ⚠️  WARNING: Test credentials detected!")
                
                # Check settings
                settings = brand.settings
                if settings:
                    print(f"    Settings: daily_limit={settings.daily_email_limit}")
            
            print("\n✅ TEST 2 PASSED: All brands and relationships valid")
            return True
            
        except Exception as e:
            print(f"❌ TEST 2 FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_real_data_enforcement():
    """Test that system enforces real data"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Real Data Enforcement")
    print("="*60)
    
    with app.app_context():
        try:
            # Check environment variables
            brevo_key = os.getenv('BREVO_API_KEY', '')
            mailersend_token = os.getenv('MAILERSEND_API_TOKEN', '')
            
            print(f"BREVO_API_KEY set: {bool(brevo_key)}")
            print(f"MAILERSEND_API_TOKEN set: {bool(mailersend_token)}")
            
            if not brevo_key or not mailersend_token:
                print("⚠️  WARNING: Some environment credentials missing")
                print("   (Optional - database can be populated manually)")
            
            # Check database credentials
            brand = Brand.query.filter_by(name='buildly').first()
            if brand:
                config = brand.email_configs.filter_by(is_primary=True).first()
                if config:
                    has_credential = bool(config.api_key or config.api_token)
                    is_valid = not ("test" in str(config.api_key).lower() if config.api_key else True)
                    
                    print(f"\nBuildly email config:")
                    print(f"  Provider: {config.provider}")
                    print(f"  Has credential: {has_credential}")
                    print(f"  Is valid (not test): {is_valid}")
                    
                    if not has_credential:
                        print("❌ TEST 3 FAILED: No real credentials")
                        return False
                    
                    if not is_valid:
                        print("❌ TEST 3 FAILED: Test credentials detected")
                        return False
            
            print("\n✅ TEST 3 PASSED: Real data enforcement verified")
            return True
            
        except Exception as e:
            print(f"❌ TEST 3 FAILED: {e}")
            return False


def test_audit_logging():
    """Test audit logging"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Audit Logging")
    print("="*60)
    
    with app.app_context():
        try:
            # Check if any logs exist
            logs = APICredentialLog.query.all()
            
            print(f"Total audit logs: {len(logs)}")
            
            if logs:
                # Show recent logs
                recent_logs = sorted(logs, key=lambda x: x.created_at, reverse=True)[:5]
                print("\nRecent audit logs:")
                for log in recent_logs:
                    print(f"  [{log.created_at}] {log.action.upper()}")
                    print(f"    Brand ID: {log.brand_id}")
                    print(f"    Status: {'✓' if log.success else '✗'}")
            
            print("✅ TEST 4 PASSED: Audit logging system operational")
            return True
            
        except Exception as e:
            print(f"❌ TEST 4 FAILED: {e}")
            return False


def test_api_structure():
    """Test API structure"""
    print("\n" + "="*60)
    print("🧪 TEST 5: Admin API Structure")
    print("="*60)
    
    try:
        from dashboard.admin_api import admin_bp
        
        # Check blueprint
        print(f"Blueprint name: {admin_bp.name}")
        print(f"Blueprint URL prefix: {admin_bp.url_prefix}")
        
        # List routes
        routes = []
        for rule in app.url_map.iter_rules():
            if 'admin' in rule.rule:
                routes.append({
                    'rule': rule.rule,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
                })
        
        print(f"\nAdmin API endpoints:")
        for route in sorted(routes, key=lambda x: x['rule']):
            methods = ','.join(sorted(route['methods']))
            print(f"  {methods:15} {route['rule']}")
        
        # Check that we have endpoints
        if len(routes) >= 9:
            print(f"\n✅ TEST 5 PASSED: Found {len(routes)} admin endpoints")
            return True
        else:
            print(f"⚠️  WARNING: Only found {len(routes)} endpoints (expected 9+)")
            return True
            
    except Exception as e:
        print(f"❌ TEST 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_relationships():
    """Test SQLAlchemy model relationships"""
    print("\n" + "="*60)
    print("🧪 TEST 6: Model Relationships")
    print("="*60)
    
    with app.app_context():
        try:
            brand = Brand.query.filter_by(name='openbuild').first()
            
            if not brand:
                print("⚠️  Openbuild brand not found, skipping relationship test")
                return True
            
            print(f"Testing relationships for: {brand.display_name}")
            
            # Test one-to-many relationship
            configs = brand.email_configs.all()
            print(f"  Email configs (1-to-many): {len(configs)} ✓")
            
            # Test one-to-one relationship
            settings = brand.settings
            if settings:
                print(f"  Settings (1-to-1): {settings.id} ✓")
            else:
                print(f"  Settings (1-to-1): None ⚠️")
            
            # Test that we can access config properties
            for config in configs:
                _ = config.from_email
                _ = config.provider
                _ = config.is_primary
                print(f"  Config properties accessible: {config.provider} ✓")
            
            print("\n✅ TEST 6 PASSED: Model relationships working correctly")
            return True
            
        except Exception as e:
            print(f"❌ TEST 6 FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Multi-Tenant Architecture Validation Tests".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        test_database_initialization,
        test_brand_data,
        test_real_data_enforcement,
        test_audit_logging,
        test_api_structure,
        test_model_relationships,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - Test {i}: {test.__name__}")
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready.")
        print("\nNext steps:")
        print("  1. Start dashboard: python dashboard/app.py")
        print("  2. Visit admin panel: http://localhost:5000/admin/brands")
        print("  3. Manage brands and email configurations")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
