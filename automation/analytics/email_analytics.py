# Email Campaign Analytics Integration
# Pulls email campaign data from various email service providers

import os
import sys
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.brand_loader import get_all_brands, get_brand_details

class EmailCampaignAnalytics:
    """Collects email campaign analytics from various providers"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.logger = logging.getLogger('EmailAnalytics')
        
        # Load brand-specific email configurations from database
        self.brand_configs = self._load_brand_configs()
    
    def _load_brand_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load brand email configurations from database with fallback"""
        configs = {}
        brands = get_all_brands(active_only=True)
        
        for brand in brands:
            brand_data = get_brand_details(brand)
            if brand_data:
                configs[brand] = {
                    'service': os.getenv(f'{brand.upper()}_EMAIL_SERVICE', 'brevo'),
                    'api_key': os.getenv(f'{brand.upper()}_EMAIL_API_KEY', ''),
                    'from_email': os.getenv(f'{brand.upper()}_FROM_EMAIL', f'team@{brand}.io'),
                    'lists': ['newsletter', 'updates', 'community']  # Default lists
                }
        
        return configs
    
    async def get_brand_email_analytics(self, brand: str, days: int = 30) -> Dict[str, Any]:
        """Get email campaign analytics for a specific brand from real API sources"""
        if brand not in self.brand_configs:
            raise ValueError(
                f"Unknown brand: {brand}. "
                f"Valid brands: {', '.join(self.brand_configs.keys())}"
            )
        
        config = self.brand_configs[brand]
        service = config['service']
        api_key = config['api_key']
        
        if not api_key:
            raise ValueError(
                f"Missing API credentials for {brand} ({service}). "
                f"Set {brand.upper()}_EMAIL_API_KEY in .env file. "
                f"Get API key from: https://www.brevo.com/settings/keys-smtp"
            )
        
        if service == 'brevo':
            return await self._get_brevo_analytics(brand, config, days)
        elif service == 'sendgrid':
            raise NotImplementedError(
                f"SendGrid integration not yet implemented for {brand}. "
                f"Currently only Brevo is supported. "
                f"Set {brand.upper()}_EMAIL_SERVICE=brevo in .env file."
            )
        elif service == 'mailgun':
            raise NotImplementedError(
                f"Mailgun integration not yet implemented for {brand}. "
                f"Currently only Brevo is supported. "
                f"Set {brand.upper()}_EMAIL_SERVICE=brevo in .env file."
            )
        else:
            raise ValueError(
                f"Unsupported email service: {service} for {brand}. "
                f"Supported services: brevo, sendgrid (coming), mailgun (coming)"
            )
    
    async def _get_brevo_analytics(self, brand: str, config: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Get analytics from Brevo (Sendinblue) - requires valid API key"""
        api_key = config['api_key']
        if not api_key:
            raise ValueError(
                f"Brevo API key missing for {brand}. "
                f"Set {brand.upper()}_EMAIL_API_KEY in .env file. "
                f"Get key from: https://www.brevo.com/settings/keys-smtp"
            )
        
        headers = {
            'api-key': api_key,
            'Content-Type': 'application/json'
        }
        
        base_url = 'https://api.brevo.com/v3'
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get campaign statistics
                campaigns_data = await self._fetch_brevo_campaigns(session, base_url, headers, days)
                
                # Get email statistics
                stats_data = await self._fetch_brevo_stats(session, base_url, headers, days)
                
                # Get contact lists info
                lists_data = await self._fetch_brevo_lists(session, base_url, headers)
        
        return {
            'brand': brand,
            'service': 'brevo',
            'period': f"Last {days} days",
            'campaigns': campaigns_data,
            'statistics': stats_data,
            'lists': lists_data,
            'last_updated': datetime.now().isoformat()
        }
    
    async def _fetch_brevo_campaigns(self, session, base_url: str, headers: Dict[str, str], days: int) -> List[Dict[str, Any]]:
        """Fetch campaign data from Brevo"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Get campaigns
            url = f"{base_url}/emailCampaigns"
            params = {
                'limit': 50,
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d')
            }
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    campaigns = []
                    
                    for campaign in data.get('campaigns', []):
                        # Get detailed statistics for each campaign
                        campaign_id = campaign['id']
                        stats_url = f"{base_url}/emailCampaigns/{campaign_id}/statistics"
                        
                        async with session.get(stats_url, headers=headers) as stats_response:
                            if stats_response.status == 200:
                                stats = await stats_response.json()
                                campaigns.append({
                                    'id': campaign_id,
                                    'name': campaign.get('name', ''),
                                    'subject': campaign.get('subject', ''),
                                    'sent_date': campaign.get('sentDate', ''),
                                    'status': campaign.get('status', ''),
                                    'sent': stats.get('delivered', 0),
                                    'delivered': stats.get('delivered', 0),
                                    'opens': stats.get('uniqueOpens', 0),
                                    'clicks': stats.get('uniqueClicks', 0),
                                    'bounces': stats.get('bounces', 0),
                                    'unsubscribes': stats.get('unsubscriptions', 0),
                                    'open_rate': stats.get('delivered', 0) and (stats.get('uniqueOpens', 0) / stats.get('delivered', 1)) * 100,
                                    'click_rate': stats.get('delivered', 0) and (stats.get('uniqueClicks', 0) / stats.get('delivered', 1)) * 100
                                })
                    
                    return campaigns
                
        except Exception as e:
            self.logger.error(f"Error fetching Brevo campaigns: {e}")
        
        return []
    
    async def _fetch_brevo_stats(self, session, base_url: str, headers: Dict[str, str], days: int) -> Dict[str, Any]:
        """Fetch overall statistics from Brevo"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            url = f"{base_url}/statistics/email"
            params = {
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d')
            }
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'total_sent': data.get('delivered', 0),
                        'total_delivered': data.get('delivered', 0),
                        'total_opens': data.get('uniqueOpens', 0),
                        'total_clicks': data.get('uniqueClicks', 0),
                        'total_bounces': data.get('bounces', 0),
                        'total_unsubscribes': data.get('unsubscriptions', 0),
                        'avg_open_rate': data.get('delivered', 0) and (data.get('uniqueOpens', 0) / data.get('delivered', 1)) * 100,
                        'avg_click_rate': data.get('delivered', 0) and (data.get('uniqueClicks', 0) / data.get('delivered', 1)) * 100
                    }
                    
        except Exception as e:
            self.logger.error(f"Error fetching Brevo stats: {e}")
        
        return {}
    
    async def _fetch_brevo_lists(self, session, base_url: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
        """Fetch contact lists from Brevo"""
        try:
            url = f"{base_url}/contacts/lists"
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    lists = []
                    
                    for list_item in data.get('lists', []):
                        lists.append({
                            'id': list_item.get('id'),
                            'name': list_item.get('name'),
                            'total_subscribers': list_item.get('totalSubscribers', 0),
                            'total_blacklisted': list_item.get('totalBlacklisted', 0),
                            'created_at': list_item.get('createdAt', '')
                        })
                    
                    return lists
                    
        except Exception as e:
            self.logger.error(f"Error fetching Brevo lists: {e}")
        
        return []
    
    async def _get_sendgrid_analytics(self, brand: str, config: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Get analytics from SendGrid (not yet implemented)"""
        raise NotImplementedError(
            f"SendGrid integration not yet implemented for {brand}. "
            f"Currently only Brevo is supported. "
            f"To use Brevo, set {brand.upper()}_EMAIL_SERVICE=brevo in .env"
        )
    
    async def _get_mailgun_analytics(self, brand: str, config: Dict[str, Any], days: int) -> Dict[str, Any]:
        """Get analytics from Mailgun (not yet implemented)"""
        raise NotImplementedError(
            f"Mailgun integration not yet implemented for {brand}. "
            f"Currently only Brevo is supported. "
            f"To use Brevo, set {brand.upper()}_EMAIL_SERVICE=brevo in .env"
        )
    
    async def get_all_brands_email_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get email analytics for all brands - requires valid API keys for each"""
        results = {}
        for brand in self.brand_configs.keys():
            try:
                results[brand] = await self.get_brand_email_analytics(brand, days)
            except ValueError as e:
                # Brand not configured - include error in results
                self.logger.warning(f"Cannot retrieve analytics for {brand}: {str(e)}")
                results[brand] = {
                    'error': str(e),
                    'brand': brand,
                    'status': 'not_configured'
                }
        
        return results

# Create global instance
email_analytics = EmailCampaignAnalytics()