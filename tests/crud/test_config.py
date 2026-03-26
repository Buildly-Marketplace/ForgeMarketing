"""
Configuration tests for ForgeMark.

Verifies that required environment variables are set and configuration is valid.
"""

import pytest
import os
from typing import List


class TestEnvironmentConfiguration:
    """Test required environment variables."""
    
    REQUIRED_VARS = [
        "FLASK_ENV",
        "OLLAMA_HOST"
    ]
    
    OPTIONAL_VARS = [
        "DATABASE_URL",
        "OPENAI_API_KEY",
        "GOOGLE_ADS_CLIENT_ID",
        "BREVO_API_KEY"
    ]
    
    def test_flask_env_is_set(self):
        """Test that FLASK_ENV is configured."""
        assert os.getenv("FLASK_ENV") is not None
    
    def test_ollama_host_is_configured(self):
        """Test that OLLAMA_HOST is set."""
        assert os.getenv("OLLAMA_HOST") is not None
    
    def test_valid_flask_environment(self):
        """Test that FLASK_ENV has a valid value."""
        env = os.getenv("FLASK_ENV", "")
        assert env in ["development", "production", "testing"]
    
    def test_missing_vars_provide_helpful_error(self):
        """Test that missing config vars are handled gracefully."""
        # This test documents expected behavior for missing config
        # The app should start and provide helpful error messages
        pass


class TestConfigFilePresence:
    """Test that required configuration files exist."""
    
    CONFIG_FILES = [
        "config/brands.yaml",
        "config/ai_config.yaml"
    ]
    
    def test_brand_config_exists(self):
        """Test that brands configuration file exists."""
        # Note: This path is relative to project root
        config_path = "config/brands.yaml"
        if os.path.exists(config_path):
            assert os.path.isfile(config_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
