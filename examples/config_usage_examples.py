"""
Configuration Management Examples
Demonstrates how to use the secure config loader instead of hardcoded credentials
"""

from config.config_loader import config_loader


class TwitterExample:
    """Example: Secure Twitter API integration"""
    
    def __init__(self, brand_name='buildly'):
        self.brand_name = brand_name
        self.credentials = None
    
    def get_credentials(self):
        """Load Twitter credentials from database"""
        self.credentials = config_loader.get_twitter_credentials(self.brand_name)
        
        if not self.credentials or not self.credentials.get('bearer_token'):
            raise ValueError(
                f"Twitter credentials not configured for {self.brand_name}. "
                "Configure via admin panel."
            )
        
        return self.credentials
    
    def get_headers(self):
        """Get authentication headers for Twitter API"""
        if not self.credentials:
            self.get_credentials()
        
        return {
            'Authorization': f'Bearer {self.credentials["bearer_token"]}',
            'Content-Type': 'application/json',
        }


class EmailExample:
    """Example: Secure email configuration"""
    
    def __init__(self, brand_name='buildly'):
        self.brand_name = brand_name
        self.config = None
    
    def get_email_config(self):
        """Load email configuration from database"""
        self.config = config_loader.get_brand_email_config(self.brand_name)
        
        if not self.config:
            raise ValueError(
                f"Email configuration not found for {self.brand_name}. "
                "Configure via admin panel."
            )
        
        return self.config
    
    def get_smtp_settings(self):
        """Get SMTP settings for email sending"""
        if not self.config:
            self.get_email_config()
        
        return {
            'host': self.config.smtp_host,
            'port': self.config.smtp_port,
            'user': self.config.smtp_user,
            'password': self.config.smtp_password,
            'from_email': self.config.from_email,
            'from_name': self.config.from_name,
        }


class AnalyticsExample:
    """Example: Secure Google Analytics integration"""
    
    def __init__(self, brand_name='buildly'):
        self.brand_name = brand_name
        self.credentials = None
    
    def get_analytics_credentials(self):
        """Load Google Analytics credentials from database"""
        self.credentials = config_loader.get_google_analytics_credentials(self.brand_name)
        
        if not self.credentials or not self.credentials.get('property_id'):
            raise ValueError(
                f"Google Analytics not configured for {self.brand_name}. "
                "Configure via admin panel."
            )
        
        return self.credentials
    
    def get_config(self):
        """Get configuration dict for analytics client"""
        if not self.credentials:
            self.get_analytics_credentials()
        
        return {
            'property_id': self.credentials['property_id'],
            'api_key': self.credentials.get('api_key', ''),
            'credentials_file': self.credentials.get('credentials_file', ''),
        }


class SystemConfigExample:
    """Example: System-wide configuration"""
    
    @staticmethod
    def get_ollama_host():
        """Get Ollama server configuration"""
        return config_loader.get_system_config(
            'OLLAMA_HOST',
            default='http://localhost:11434',
            category='ai'
        )
    
    @staticmethod
    def get_ollama_model():
        """Get default Ollama model"""
        return config_loader.get_system_config(
            'OLLAMA_MODEL',
            default='llama3.2:1b',
            category='ai'
        )
    
    @staticmethod
    def get_flask_env():
        """Get Flask environment"""
        return config_loader.get_system_config(
            'FLASK_ENV',
            default='production',
            category='system'
        )


class ConfigManagementExample:
    """Example: Managing configuration via code"""
    
    @staticmethod
    def add_twitter_credentials(brand_name, credentials):
        """Add Twitter credentials for a brand"""
        success = config_loader.set_brand_api_credential(
            brand_name=brand_name,
            service='twitter',
            credential_type='oauth',
            credentials={
                'api_key': credentials['api_key'],
                'api_secret': credentials['api_secret'],
                'access_token': credentials['access_token'],
                'access_token_secret': credentials['access_token_secret'],
                'bearer_token': credentials['bearer_token'],
            }
        )
        
        if success:
            print(f"✓ Twitter credentials added for {brand_name}")
        else:
            print(f"✗ Failed to add Twitter credentials for {brand_name}")
        
        return success
    
    @staticmethod
    def add_system_config(key, value, description='', is_secret=False):
        """Add system configuration"""
        success = config_loader.set_system_config(
            key=key,
            value=value,
            description=description,
            is_secret=is_secret,
            category='general'
        )
        
        if success:
            print(f"✓ System config '{key}' set")
        else:
            print(f"✗ Failed to set system config '{key}'")
        
        return success


# Usage Examples
if __name__ == '__main__':
    # Example 1: Twitter Integration
    print("Example 1: Twitter Integration")
    try:
        twitter = TwitterExample('buildly')
        headers = twitter.get_headers()
        print(f"✓ Twitter headers loaded successfully")
    except ValueError as e:
        print(f"✗ {e}")
    
    # Example 2: Email Configuration
    print("\nExample 2: Email Configuration")
    try:
        email = EmailExample('buildly')
        smtp = email.get_smtp_settings()
        print(f"✓ SMTP settings loaded: {smtp['host']}:{smtp['port']}")
    except ValueError as e:
        print(f"✗ {e}")
    
    # Example 3: Google Analytics
    print("\nExample 3: Google Analytics")
    try:
        analytics = AnalyticsExample('buildly')
        config = analytics.get_config()
        print(f"✓ Analytics configured for property: {config['property_id']}")
    except ValueError as e:
        print(f"✗ {e}")
    
    # Example 4: System Configuration
    print("\nExample 4: System Configuration")
    ollama_host = SystemConfigExample.get_ollama_host()
    ollama_model = SystemConfigExample.get_ollama_model()
    print(f"✓ Ollama: {ollama_host} using {ollama_model}")
