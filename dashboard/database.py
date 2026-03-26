"""
Database initialization and migration utilities
"""

import os
from pathlib import Path
from datetime import datetime
from dashboard.models import db, Brand, BrandEmailConfig, BrandSettings, BrandAPICredential, SystemConfig, APICredentialLog


class DatabaseManager:
    """Manages database initialization and migrations"""
    
    def __init__(self, app):
        self.app = app
        self.db_path = Path(app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///dashboard.db').replace('sqlite:///', ''))
    
    def init_db(self) -> bool:
        """Initialize database with schema (no default brands)"""
        try:
            with self.app.app_context():
                db.create_all()
                print("✅ Database schema initialized successfully")
                
                # No longer auto-loading default brands
                # Brands are created through onboarding or admin panel
                brand_count = Brand.query.count()
                if brand_count == 0:
                    print("ℹ️  No brands configured. Complete onboarding to add brands.")
                else:
                    print(f"✅ Found {brand_count} existing brand(s)")
                
                return True
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False
    
    def _load_default_brands(self) -> None:
        """Load default brands from environment"""
        import os
        
        brands_data = [
            {
                'name': 'buildly',
                'display_name': 'Buildly',
                'description': 'Project management platform',
                'website_url': 'https://buildly.io',
                'email_config': {
                    'provider': 'mailersend',
                    'api_key': os.getenv('MAILERSEND_API_TOKEN', ''),
                    'from_email': os.getenv('BUILDLY_FROM_EMAIL', 'team@buildly.io'),
                    'from_name': 'Buildly Team'
                }
            },
            {
                'name': 'foundry',
                'display_name': 'Foundry',
                'description': 'Startup accelerator platform',
                'website_url': 'https://firstcityfoundry.com',
                'email_config': {
                    'provider': 'brevo',
                    'api_key': os.getenv('BREVO_API_KEY', ''),
                    'from_email': os.getenv('FOUNDRY_FROM_EMAIL', 'team@firstcityfoundry.com'),
                    'from_name': 'Foundry Team'
                }
            },
            {
                'name': 'openbuild',
                'display_name': 'OpenBuild',
                'description': 'Community-driven development platform',
                'website_url': 'https://open.build',
                'email_config': {
                    'provider': 'brevo',
                    'api_key': os.getenv('BREVO_API_KEY', ''),
                    'from_email': os.getenv('OPEN_BUILD_FROM_EMAIL', 'team@open.build'),
                    'from_name': 'OpenBuild Team'
                }
            },
            {
                'name': 'radical',
                'display_name': 'Radical Therapy',
                'description': 'Digital therapy platform',
                'website_url': 'https://radicaltherapy.com',
                'email_config': {
                    'provider': 'brevo',
                    'api_key': os.getenv('BREVO_API_KEY', ''),
                    'from_email': os.getenv('RADICAL_THERAPY_FROM_EMAIL', 'team@radicaltherapy.com'),
                    'from_name': 'Radical Therapy'
                }
            },
            {
                'name': 'oregonsoftware',
                'display_name': 'Oregon Software',
                'description': 'Software development services',
                'website_url': 'https://oregonsoftware.com',
                'email_config': {
                    'provider': 'brevo',
                    'api_key': os.getenv('BREVO_API_KEY', ''),
                    'from_email': os.getenv('OREGON_SOFTWARE_FROM_EMAIL', 'team@oregonsoftware.com'),
                    'from_name': 'Oregon Software'
                }
            }
        ]
        
        for brand_data in brands_data:
            try:
                # Create brand
                brand = Brand(
                    name=brand_data['name'],
                    display_name=brand_data['display_name'],
                    description=brand_data['description'],
                    website_url=brand_data['website_url'],
                    is_active=True
                )
                db.session.add(brand)
                db.session.flush()  # Get the brand ID
                
                # Create email config
                if brand_data['email_config']['api_key']:
                    email_config = BrandEmailConfig(
                        brand_id=brand.id,
                        provider=brand_data['email_config']['provider'],
                        api_key=brand_data['email_config']['api_key'],
                        from_email=brand_data['email_config']['from_email'],
                        from_name=brand_data['email_config']['from_name'],
                        is_primary=True,
                        is_verified=True
                    )
                    db.session.add(email_config)
                
                # Create settings
                settings = BrandSettings(brand_id=brand.id)
                db.session.add(settings)
                
                print(f"✅ Created brand: {brand_data['display_name']}")
            except Exception as e:
                print(f"⚠️  Failed to create brand {brand_data['display_name']}: {e}")
        
        try:
            db.session.commit()
            print(f"✅ Loaded {Brand.query.count()} default brands")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Failed to commit brands: {e}")
    
    def reset_db(self) -> bool:
        """Drop all tables and recreate (DESTRUCTIVE!)"""
        try:
            with self.app.app_context():
                db.drop_all()
                db.create_all()
                self._load_default_brands()
                print("✅ Database reset successfully")
                return True
        except Exception as e:
            print(f"❌ Database reset failed: {e}")
            return False
    
    @staticmethod
    def backup_db(source_path: str, backup_path: str) -> bool:
        """Backup SQLite database"""
        try:
            import shutil
            shutil.copy(source_path, backup_path)
            print(f"✅ Database backed up to {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
