"""
Database-Aware Email Campaign Analytics
Pulls email campaign data from various email service providers using database configuration
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

# Try to import database models
try:
    from dashboard.models import Brand, BrandEmailConfig
    HAS_DB_MODELS = True
except ImportError:
    HAS_DB_MODELS = False


class DatabaseEmailAnalytics:
    """Collects email campaign analytics using database-backed configuration"""
    
    def __init__(self, app=None):
        self.project_root = Path(__file__).parent.parent.parent
        self.logger = logging.getLogger('EmailAnalytics')
        self.app = app
        
        # Brevo API configuration
        self.brevo_api_base = "https://api.brevo.com/v3"
        self.brevo_timeout = aiohttp.ClientTimeout(total=30)
        
        # MailerSend API configuration
        self.mailersend_api_base = "https://api.mailersend.com/v1"
        self.mailersend_timeout = aiohttp.ClientTimeout(total=30)
    
    def get_brand_config(self, brand_name: str) -> Optional[Dict[str, Any]]:
        """Get brand configuration from database"""
        if not HAS_DB_MODELS:
            raise RuntimeError("Database models not available. Cannot use DatabaseEmailAnalytics.")
        
        try:
            brand = Brand.query.filter_by(name=brand_name).first()
            if not brand:
                raise ValueError(
                    f"Unknown brand: {brand_name}. "
                    f"Create brand through admin panel at /admin/brands"
                )
            
            # Get primary email config
            email_config = brand.email_configs.filter_by(is_primary=True).first()
            if not email_config:
                raise ValueError(
                    f"No primary email configuration for brand {brand_name}. "
                    f"Add email provider through admin panel at /admin/brands/{brand_name}/email-configs"
                )
            
            if not email_config.api_key and not email_config.api_token:
                raise ValueError(
                    f"Missing API credentials for {brand_name} ({email_config.provider}). "
                    f"Configure credentials through admin panel."
                )
            
            return {
                'brand_name': brand.name,
                'display_name': brand.display_name,
                'provider': email_config.provider,
                'api_key': email_config.api_key,
                'api_token': email_config.api_token,
                'from_email': email_config.from_email,
                'from_name': email_config.from_name,
                'is_verified': email_config.is_verified,
                'contact_lists': email_config.get_contact_lists() if hasattr(email_config, 'get_contact_lists') else {}
            }
        except Exception as e:
            self.logger.error(f"Error getting brand config for {brand_name}: {e}")
            raise
    
    async def get_brand_email_analytics(self, brand: str, days: int = 30) -> Dict[str, Any]:
        """
        Get email campaign analytics for a specific brand from real API sources
        Uses database configuration instead of environment variables
        """
        try:
            config = self.get_brand_config(brand)
        except ValueError as e:
            self.logger.error(f"Configuration error for {brand}: {e}")
            raise
        
        provider = config['provider']
        
        if provider == 'brevo':
            return await self._get_brevo_analytics(brand, config, days)
        elif provider == 'mailersend':
            return await self._get_mailersend_analytics(brand, config, days)
        elif provider == 'sendgrid':
            raise NotImplementedError(
                f"SendGrid integration not yet implemented. "
                f"Use Brevo or MailerSend instead."
            )
        elif provider == 'mailgun':
            raise NotImplementedError(
                f"Mailgun integration not yet implemented. "
                f"Use Brevo or MailerSend instead."
            )
        else:
            raise ValueError(
                f"Unsupported email provider: {provider}. "
                f"Supported providers: brevo, mailersend"
            )
    
    async def _get_brevo_analytics(self, brand: str, config: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Get analytics from Brevo API"""
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
            end_date = datetime.utcnow().strftime('%Y-%m-%d')
            
            headers = {
                'api-key': config['api_key'],
                'Content-Type': 'application/json'
            }
            
            # Get statistics endpoint
            url = f"{self.brevo_api_base}/smtp/statistics"
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            async with aiohttp.ClientSession(timeout=self.brevo_timeout) as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Brevo API error: {response.status} - {error_text}")
                    
                    data = await response.json()
                    
                    return {
                        'brand': brand,
                        'provider': 'brevo',
                        'analytics': data,
                        'period': {
                            'start': start_date,
                            'end': end_date,
                            'days': days
                        },
                        'retrieved_at': datetime.utcnow().isoformat(),
                        'from_email': config['from_email']
                    }
        except Exception as e:
            self.logger.error(f"Error getting Brevo analytics for {brand}: {e}")
            raise
    
    async def _get_mailersend_analytics(self, brand: str, config: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Get analytics from MailerSend API"""
        try:
            start_date = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
            end_date = datetime.utcnow().strftime('%Y-%m-%d')
            
            headers = {
                'Authorization': f'Bearer {config["api_token"]}',
                'Content-Type': 'application/json'
            }
            
            # MailerSend analytics endpoint
            url = f"{self.mailersend_api_base}/analytics"
            params = {
                'date_from': int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()),
                'date_to': int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
            }
            
            async with aiohttp.ClientSession(timeout=self.mailersend_timeout) as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"MailerSend API error: {response.status} - {error_text}")
                    
                    data = await response.json()
                    
                    return {
                        'brand': brand,
                        'provider': 'mailersend',
                        'analytics': data,
                        'period': {
                            'start': start_date,
                            'end': end_date,
                            'days': days
                        },
                        'retrieved_at': datetime.utcnow().isoformat(),
                        'from_email': config['from_email']
                    }
        except Exception as e:
            self.logger.error(f"Error getting MailerSend analytics for {brand}: {e}")
            raise
    
    async def get_all_brands_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics for all brands"""
        if not HAS_DB_MODELS:
            raise RuntimeError("Database models not available.")
        
        analytics = {}
        brands = Brand.query.filter_by(is_active=True).all()
        
        for brand in brands:
            try:
                analytics[brand.name] = await self.get_brand_email_analytics(brand.name, days)
            except Exception as e:
                self.logger.error(f"Failed to get analytics for {brand.name}: {e}")
                analytics[brand.name] = {
                    'error': str(e),
                    'brand': brand.name
                }
        
        return {
            'all_brands': analytics,
            'period_days': days,
            'retrieved_at': datetime.utcnow().isoformat()
        }
    
    async def verify_provider_credentials(self, brand_name: str) -> Dict[str, Any]:
        """Verify that provider credentials are valid"""
        try:
            config = self.get_brand_config(brand_name)
            provider = config['provider']
            
            if provider == 'brevo':
                return await self._verify_brevo_credentials(config)
            elif provider == 'mailersend':
                return await self._verify_mailersend_credentials(config)
            else:
                return {
                    'valid': False,
                    'error': f"Verification not implemented for {provider}"
                }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    async def _verify_brevo_credentials(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Verify Brevo API credentials"""
        try:
            headers = {
                'api-key': config['api_key'],
                'Content-Type': 'application/json'
            }
            
            url = f"{self.brevo_api_base}/account"
            
            async with aiohttp.ClientSession(timeout=self.brevo_timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'valid': True,
                            'provider': 'brevo',
                            'account_email': data.get('email', 'Unknown')
                        }
                    else:
                        error_text = await response.text()
                        return {
                            'valid': False,
                            'provider': 'brevo',
                            'error': f"API error: {response.status}"
                        }
        except Exception as e:
            return {
                'valid': False,
                'provider': 'brevo',
                'error': str(e)
            }
    
    async def _verify_mailersend_credentials(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Verify MailerSend API credentials"""
        try:
            headers = {
                'Authorization': f'Bearer {config["api_token"]}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.mailersend_api_base}/domains"
            
            async with aiohttp.ClientSession(timeout=self.mailersend_timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'valid': True,
                            'provider': 'mailersend',
                            'domains': len(data.get('data', []))
                        }
                    else:
                        return {
                            'valid': False,
                            'provider': 'mailersend',
                            'error': f"API error: {response.status}"
                        }
        except Exception as e:
            return {
                'valid': False,
                'provider': 'mailersend',
                'error': str(e)
            }


# For backwards compatibility, also export the database-aware version as the main class
EmailCampaignAnalytics = DatabaseEmailAnalytics
