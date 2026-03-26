"""
CRUD smoke tests for ForgeMark.

Verifies basic create, read, update, delete operations on core resources.
"""

import pytest
import requests
import json
from typing import Dict, Any


class TestCampaignCRUD:
    """Test campaign create, read, update, delete operations."""
    
    BASE_URL = "http://localhost:5000"
    CAMPAIGNS_ENDPOINT = f"{BASE_URL}/api/campaigns"
    
    @staticmethod
    def create_campaign() -> Dict[str, Any]:
        """Create a test campaign."""
        payload = {
            "name": "Smoke Test Campaign",
            "brand_slug": "buildly",
            "status": "draft",
            "content": "Test content for smoke test"
        }
        response = requests.post(TestCampaignCRUD.CAMPAIGNS_ENDPOINT, json=payload)
        assert response.status_code in [200, 201], f"Failed to create campaign: {response.text}"
        return response.json()
    
    def test_create_campaign(self):
        """Test creating a new campaign."""
        campaign = self.create_campaign()
        assert "id" in campaign or "id" in campaign
        assert campaign.get("name") == "Smoke Test Campaign"
    
    def test_read_campaigns(self):
        """Test reading list of campaigns."""
        response = requests.get(self.CAMPAIGNS_ENDPOINT)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))
    
    def test_read_single_campaign(self):
        """Test reading a single campaign."""
        campaign = self.create_campaign()
        campaign_id = campaign.get("id")
        
        response = requests.get(f"{self.CAMPAIGNS_ENDPOINT}/{campaign_id}")
        assert response.status_code == 200
        retrieved = response.json()
        assert retrieved.get("id") == campaign_id
    
    def test_update_campaign(self):
        """Test updating an existing campaign."""
        campaign = self.create_campaign()
        campaign_id = campaign.get("id")
        
        update_payload = {
            "name": "Updated Campaign Name",
            "status": "active"
        }
        response = requests.put(
            f"{self.CAMPAIGNS_ENDPOINT}/{campaign_id}",
            json=update_payload
        )
        assert response.status_code in [200, 204]
    
    def test_delete_campaign(self):
        """Test deleting a campaign."""
        campaign = self.create_campaign()
        campaign_id = campaign.get("id")
        
        response = requests.delete(f"{self.CAMPAIGNS_ENDPOINT}/{campaign_id}")
        assert response.status_code in [200, 204, 404]  # 404 is OK if not found


class TestContentGeneration:
    """Test content generation endpoint."""
    
    BASE_URL = "http://localhost:5000"
    GENERATE_ENDPOINT = f"{BASE_URL}/api/content/generate"
    
    def test_content_generation_endpoint_exists(self):
        """Test that content generation endpoint is available."""
        payload = {
            "brand_slug": "buildly",
            "content_type": "social_post",
            "topic": "AI automation"
        }
        response = requests.post(self.GENERATE_ENDPOINT, json=payload)
        # Endpoint should exist (200, 201, or 400 for validation, not 404)
        assert response.status_code != 404


class TestAnalytics:
    """Test analytics endpoints."""
    
    BASE_URL = "http://localhost:5000"
    ANALYTICS_ENDPOINT = f"{BASE_URL}/api/analytics/dashboard"
    
    def test_analytics_dashboard_endpoint_exists(self):
        """Test that analytics dashboard endpoint is available."""
        response = requests.get(self.ANALYTICS_ENDPOINT)
        # Endpoint should exist (not 404)
        assert response.status_code != 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
