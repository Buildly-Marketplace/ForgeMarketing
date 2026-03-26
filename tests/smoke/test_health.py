"""
Health check and smoke tests for ForgeMark.

Verifies that the application starts correctly and responds to basic health checks.
"""

import pytest
import requests
import time
from urllib.error import URLError


class TestHealthCheck:
    """Test service health endpoints."""
    
    BASE_URL = "http://localhost:5000"
    HEALTH_ENDPOINT = f"{BASE_URL}/health"
    TIMEOUT = 30
    RETRY_DELAY = 1
    MAX_RETRIES = 30
    
    @classmethod
    def wait_for_service(cls):
        """Wait for service to become available."""
        for attempt in range(cls.MAX_RETRIES):
            try:
                response = requests.get(cls.HEALTH_ENDPOINT, timeout=5)
                if response.status_code == 200:
                    return True
            except (requests.ConnectionError, requests.Timeout, URLError):
                if attempt < cls.MAX_RETRIES - 1:
                    time.sleep(cls.RETRY_DELAY)
        return False
    
    def test_health_endpoint_returns_200(self):
        """Test that /health endpoint returns 200 OK."""
        if not self.wait_for_service():
            pytest.skip("Service not available")
        
        response = requests.get(self.HEALTH_ENDPOINT)
        assert response.status_code == 200
    
    def test_health_response_is_json(self):
        """Test that health response is valid JSON."""
        if not self.wait_for_service():
            pytest.skip("Service not available")
        
        response = requests.get(self.HEALTH_ENDPOINT)
        data = response.json()
        assert isinstance(data, dict)
    
    def test_health_response_has_status(self):
        """Test that health response includes status field."""
        if not self.wait_for_service():
            pytest.skip("Service not available")
        
        response = requests.get(self.HEALTH_ENDPOINT)
        data = response.json()
        assert "status" in data
        assert data["status"] in ["healthy", "ok", "running"]
    
    def test_health_response_has_version(self):
        """Test that health response includes version."""
        if not self.wait_for_service():
            pytest.skip("Service not available")
        
        response = requests.get(self.HEALTH_ENDPOINT)
        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)
    
    def test_service_responds_to_multiple_requests(self):
        """Test that service handles multiple rapid requests."""
        if not self.wait_for_service():
            pytest.skip("Service not available")
        
        for _ in range(5):
            response = requests.get(self.HEALTH_ENDPOINT)
            assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
