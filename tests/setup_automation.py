#!/usr/bin/env python3
"""
Marketing Automation Setup Script
Complete initialization and configuration for the unified marketing system
"""

import os
import sys
import asyncio
from pathlib import Path
import subprocess
import yaml

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_banner():
    """Print setup banner"""
    print("🚀 Marketing Automation System Setup")
    print("=" * 50)
    print("Unified AI-powered marketing automation for:")
    print("  • Buildly - AI product development platform")
    print("  • The Foundry - Startup incubator")
    print("  • Open Build - Developer community")
    print("  • Radical Therapy - Programming methodology")
    print()

def check_requirements():
    """Check system requirements"""
    print("🔍 Checking System Requirements")
    print("-" * 30)
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} - Need Python 3.8+")
        return False
    
    # Check if Ollama is accessible
    try:
        import requests
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        response = requests.get(f"{ollama_host}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama connection ({len(models)} models available)")
        else:
            print(f"❌ Ollama not accessible at {ollama_host}")
            print("   Make sure Ollama is running and accessible")
            return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False
    
    # Check required packages
    required_packages = ['aiohttp', 'yaml', 'requests', 'pathlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'yaml':
                import yaml
            elif package == 'pathlib':
                import pathlib
            elif package == 'aiohttp':
                import aiohttp
            elif package == 'requests':
                import requests
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - missing")
            missing_packages.append(package if package != 'yaml' else 'pyyaml')
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All requirements met!")
    return True

def create_directory_structure():
    """Create complete directory structure"""
    print("\n📁 Creating Directory Structure")
    print("-" * 30)
    
    directories = [
        # Core automation directories
        'automation',
        'automation/ai',
        'automation/social_media',
        'automation/outreach',
        'automation/analytics',
        'automation/scheduling',
        
        # Data directories
        'data',
        'data/analytics',
        'data/contacts',
        'data/campaigns',
        'data/content',
        
        # Configuration
        'config',
        'config/secrets',
        
        # Templates
        'templates',
        'templates/brands',
        'templates/brands/buildly',
        'templates/brands/foundry',
        'templates/brands/open_build',
        'templates/brands/radical_therapy',
        'templates/email',
        'templates/social',
        'templates/blog',
        
        # Reports and logs
        'reports',
        'logs',
        
        # Dashboard and web interface
        'dashboard',
        'dashboard/static',
        'dashboard/templates',
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")
        else:
            print(f"📁 Exists: {directory}")

async def test_ai_integration():
    """Test AI integration"""
    print("\n🧠 Testing AI Integration")
    print("-" * 25)
    
    try:
        from automation.ai.ollama_integration import OllamaClient, AIContentGenerator
        
        # Test Ollama connection
        client = OllamaClient()
        connected = await client.test_connection()
        
        if connected:
            print("✅ Ollama connection successful")
            
            # Test content generation
            generator = AIContentGenerator()
            brands = list(generator.brand_configs.keys())
            
            if brands:
                print(f"✅ Brand configurations loaded: {', '.join(brands)}")
                
                # Test quick generation
                test_brand = brands[0]
                try:
                    content = await client.generate(
                        model="llama3.2:1b",
                        prompt="Write a one sentence description of AI in software development.",
                        max_tokens=50
                    )
                    if content:
                        print("✅ AI content generation working")
                        return True
                    else:
                        print("❌ AI content generation failed")
                        return False
                except Exception as e:
                    print(f"❌ AI generation error: {e}")
                    return False
            else:
                print("⚠️  No brand configurations found")
                return False
        else:
            print("❌ Ollama connection failed")
            return False
            
    except Exception as e:
        print(f"❌ AI integration error: {e}")
        return False

def create_brand_configurations():
    """Create missing brand configurations"""
    print("\n🎨 Setting Up Brand Configurations")
    print("-" * 35)
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_python_version():
    """Check if Python 3.8+ is available"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, but found {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Set up Python virtual environment"""
    venv_path = Path('.venv')
    
    if venv_path.exists():
        print("📦 Virtual environment already exists")
        return True
    
    success = run_command('python3 -m venv .venv', 'Creating virtual environment')
    if not success:
        return False
    
    # Activate and upgrade pip
    if os.name == 'nt':  # Windows
        activate_cmd = '.venv\\Scripts\\activate'
        pip_cmd = '.venv\\Scripts\\pip'
    else:  # Unix/macOS
        activate_cmd = 'source .venv/bin/activate'
        pip_cmd = '.venv/bin/pip'
    
    success = run_command(f'{pip_cmd} install --upgrade pip', 'Upgrading pip')
    return success

def install_requirements():
    """Install Python requirements"""
    requirements_file = Path('requirements.txt')
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    if os.name == 'nt':  # Windows
        pip_cmd = '.venv\\Scripts\\pip'
    else:  # Unix/macOS
        pip_cmd = '.venv/bin/pip'
    
    success = run_command(f'{pip_cmd} install -r requirements.txt', 'Installing Python packages')
    return success

def setup_configuration():
    """Set up configuration files"""
    config_dir = Path('config')
    
    # Create .env file if it doesn't exist
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env configuration file")
        env_content = """# Marketing Automation Configuration
# Copy this file and update with your actual credentials

# Twitter API Credentials
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# Email Configuration (Brevo SMTP)
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=your_smtp_user
BREVO_SMTP_PASSWORD=your_smtp_password

# Google Analytics
GOOGLE_ANALYTICS_PROPERTY_ID=G-YFY5W80XQX

# System Settings
LOG_LEVEL=INFO
DEBUG_MODE=False

# Team Notifications
TEAM_EMAIL=team@open.build
NOTIFICATION_EMAILS=team@open.build

# Rate Limiting
MAX_DAILY_EMAILS=60
MAX_SOCIAL_POSTS_PER_DAY=20
MIN_DELAY_SECONDS=30
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("⚠️  IMPORTANT: Edit .env file with your actual credentials!")
    
    return True

def create_initial_databases():
    """Create initial SQLite databases"""
    data_dir = Path('data/databases')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create empty database files
    databases = [
        'contacts.db',
        'campaigns.db', 
        'analytics.db',
        'content.db'
    ]
    
    for db_name in databases:
        db_path = data_dir / db_name
        if not db_path.exists():
            # Create empty SQLite database
            import sqlite3
            conn = sqlite3.connect(db_path)
            conn.execute('CREATE TABLE IF NOT EXISTS metadata (key TEXT, value TEXT)')
            conn.execute('INSERT INTO metadata (key, value) VALUES (?, ?)', 
                        ('created_at', str(Path(__file__).stat().st_mtime)))
            conn.commit()
            conn.close()
            print(f"📊 Created database: {db_name}")
    
    return True

def setup_logging():
    """Set up logging directories"""
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    # Create initial log files
    log_files = [
        'dashboard.log',
        'automation.log',
        'social_automation.log',
        'website_monitor.log',
        'errors.log'
    ]
    
    for log_file in log_files:
        log_path = logs_dir / log_file
        if not log_path.exists():
            log_path.touch()
    
    print("📝 Logging directories set up")
    return True

def test_system():
    """Test basic system functionality"""
    print("🧪 Testing system setup...")
    
    # Test Python imports
    try:
        if os.name == 'nt':  # Windows
            python_cmd = '.venv\\Scripts\\python'
        else:  # Unix/macOS
            python_cmd = '.venv/bin/python'
        
        test_command = f'{python_cmd} -c "import sys, os, sqlite3, json, datetime; print(\\"✅ Core imports working\\")"'
        success = run_command(test_command, 'Testing core Python imports')
        
        if not success:
            return False
        
        # Test dashboard controller
        controller_path = Path('dashboard/main_controller.py')
        if controller_path.exists():
            test_controller = f'{python_cmd} -c "import sys; sys.path.insert(0, \'dashboard\'); from main_controller import MarketingController; print(\\"✅ Controller imports working\\")"'
            run_command(test_controller, 'Testing main controller')
        
        print("✅ System test completed")
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Marketing Automation System Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ('Virtual Environment', setup_virtual_environment),
        ('Python Requirements', install_requirements),
        ('Configuration Files', setup_configuration),
        ('Database Setup', create_initial_databases),
        ('Logging Setup', setup_logging),
        ('System Test', test_system)
    ]
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}")
        print("-" * 30)
        
        if not step_function():
            print(f"❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n🎉 Marketing Automation System Setup Complete!")
    print("\nNext Steps:")
    print("1. Edit .env file with your actual API credentials")
    print("2. Test the system: python dashboard/main_controller.py") 
    print("3. Run daily automation: python dashboard/main_controller.py")
    print("4. Access dashboard: python dashboard/web_interface.py")
    print("\nDocumentation:")
    print("- PROJECT_CONTEXT.md - Complete system overview")
    print("- CLEAN_SEPARATION_PLAN.md - Architecture details")
    print("- config/ - Configuration files")

if __name__ == "__main__":
    main()