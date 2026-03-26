"""
Brand Loader Utility
Replaces hardcoded brand lists with database queries
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from functools import lru_cache

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class BrandLoader:
    """Load brand data from database instead of hardcoded values"""
    
    def __init__(self, app=None):
        """Initialize brand loader with Flask app context"""
        self.app = app
        self._brands_cache = None
        self._cache_timestamp = None
        
    def _get_app(self):
        """Get Flask app, creating it if necessary"""
        if self.app:
            return self.app
            
        # Import here to avoid circular dependency
        try:
            from dashboard.app import create_app
            self.app = create_app()
            return self.app
        except Exception as e:
            print(f"⚠️  Warning: Could not create Flask app: {e}")
            print("   Falling back to default brands")
            return None
    
    def get_all_brands(self, active_only: bool = True, include_details: bool = False) -> List[str]:
        """
        Get list of all brand names from database
        
        Args:
            active_only: Only return active brands (default True)
            include_details: Return full brand objects instead of just names
            
        Returns:
            List of brand names from database
            or list of brand dictionaries if include_details=True
            Empty list if database unavailable
        """
        app = self._get_app()
        
        if not app:
            print("❌ ERROR: Database not available. Cannot load brands.")
            print("   Please ensure the database is initialized and accessible.")
            return []
        
        try:
            with app.app_context():
                from dashboard.models import Brand
                
                query = Brand.query
                if active_only:
                    query = query.filter_by(is_active=True)
                
                brands = query.order_by(Brand.name).all()
                
                if include_details:
                    return [brand.to_dict() for brand in brands]
                else:
                    return [brand.name for brand in brands]
        except Exception as e:
            print(f"❌ ERROR: Failed to load brands from database: {e}")
            print("   Please check database connection and schema.")
            return []
    
    def get_brand_by_name(self, brand_name: str) -> Optional[Dict[str, Any]]:
        """
        Get brand details by name
        
        Args:
            brand_name: Brand identifier (e.g., 'buildly', 'foundry')
            
        Returns:
            Brand dictionary or None if not found
        """
        app = self._get_app()
        
        if not app:
            return None
        
        try:
            with app.app_context():
                from dashboard.models import Brand
                brand = Brand.query.filter_by(name=brand_name).first()
                return brand.to_dict() if brand else None
        except Exception as e:
            print(f"⚠️  Error loading brand '{brand_name}': {e}")
            return None
    
    def get_brand_config(self, brand_name: str, config_type: str = 'all') -> Dict[str, Any]:
        """
        Get brand configuration including credentials and settings
        
        Args:
            brand_name: Brand identifier
            config_type: 'email', 'api', 'settings', or 'all'
            
        Returns:
            Configuration dictionary
        """
        app = self._get_app()
        
        if not app:
            return {}
        
        try:
            with app.app_context():
                from dashboard.models import Brand, BrandEmailConfig, BrandSettings, BrandAPICredential
                
                brand = Brand.query.filter_by(name=brand_name).first()
                if not brand:
                    return {}
                
                config = {'brand': brand.to_dict()}
                
                if config_type in ['email', 'all']:
                    email_configs = BrandEmailConfig.query.filter_by(brand_id=brand.id).all()
                    config['email'] = [
                        {
                            'provider': ec.provider,
                            'from_email': ec.from_email,
                            'from_name': ec.from_name,
                            'is_primary': ec.is_primary
                        }
                        for ec in email_configs
                    ]
                
                if config_type in ['settings', 'all']:
                    settings = BrandSettings.query.filter_by(brand_id=brand.id).first()
                    if settings:
                        config['settings'] = {
                            'website_url': brand.website_url,
                            'description': brand.description
                        }
                
                if config_type in ['api', 'all']:
                    api_creds = BrandAPICredential.query.filter_by(brand_id=brand.id).all()
                    config['services'] = [cred.service for cred in api_creds]
                
                return config
        except Exception as e:
            print(f"⚠️  Error loading config for '{brand_name}': {e}")
            return {}
    
    def is_brand_active(self, brand_name: str) -> bool:
        """Check if a brand is active in the database"""
        app = self._get_app()
        
        if not app:
            print(f"❌ ERROR: Database not available. Cannot check brand '{brand_name}'.")
            return False
        
        try:
            with app.app_context():
                from dashboard.models import Brand
                brand = Brand.query.filter_by(name=brand_name, is_active=True).first()
                return brand is not None
        except Exception as e:
            print(f"❌ ERROR: Failed to check brand status: {e}")
            return False
    
    def get_brand_mapping(self) -> Dict[str, str]:
        """
        Get mapping of brand names to display names
        
        Returns:
            Dictionary like {'brand_name': 'Brand Display Name', ...}
            Empty dict if database unavailable
        """
        brands = self.get_all_brands(include_details=True)
        
        if not brands:
            print("❌ ERROR: No brands available from database.")
            return {}
        
        if isinstance(brands, list) and len(brands) > 0 and isinstance(brands[0], dict):
            return {b['name']: b['display_name'] for b in brands}
        else:
            print("❌ ERROR: Invalid brand data format.")
            return {}


# Global singleton instance
_brand_loader = None


def get_brand_loader(app=None) -> BrandLoader:
    """Get or create the global brand loader instance"""
    global _brand_loader
    if _brand_loader is None:
        _brand_loader = BrandLoader(app)
    elif app is not None and _brand_loader.app is None:
        _brand_loader.app = app
    return _brand_loader


def get_all_brands(active_only: bool = True) -> List[str]:
    """
    Convenience function to get all brand names
    
    Usage:
        from config.brand_loader import get_all_brands
        brands = get_all_brands()  # Returns ['buildly', 'foundry', ...]
    """
    loader = get_brand_loader()
    return loader.get_all_brands(active_only=active_only)


def get_brand_details(brand_name: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get brand details
    
    Usage:
        from config.brand_loader import get_brand_details
        brand = get_brand_details('buildly')
    """
    loader = get_brand_loader()
    return loader.get_brand_by_name(brand_name)


# Export key functions
__all__ = ['BrandLoader', 'get_brand_loader', 'get_all_brands', 'get_brand_details']
