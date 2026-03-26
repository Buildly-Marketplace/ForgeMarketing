#!/usr/bin/env python3
"""
Initialize the database with default brands and configurations
Run this once to set up the database for the first time
"""

import os
import sys
from pathlib import Path

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
from dashboard.database import DatabaseManager

def main():
    """Initialize database"""
    print("🚀 Initializing Marketing Dashboard Database...")
    
    with app.app_context():
        try:
            # Initialize database manager
            db_manager = DatabaseManager(app)
            
            # Initialize database
            success = db_manager.init_db()
            
            if success:
                print("\n✅ Database initialization complete!")
                print("📊 Database location:", app.config['SQLALCHEMY_DATABASE_URI'])
                
                # Show loaded brands
                from dashboard.models import Brand
                brands = Brand.query.all()
                print(f"\n📋 Loaded {len(brands)} brands:")
                for brand in brands:
                    print(f"   • {brand.display_name} ({brand.name})")
                    configs = brand.email_configs.all()
                    for config in configs:
                        print(f"     - {config.provider} (from: {config.from_email})")
            else:
                print("\n❌ Database initialization failed")
                sys.exit(1)
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
