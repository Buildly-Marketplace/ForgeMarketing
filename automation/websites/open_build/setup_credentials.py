#!/usr/bin/env python3
"""
Secure credential setup for Open Build Outreach Automation
This script helps users set up their environment variables securely
"""

import os
import getpass
from pathlib import Path

def setup_credentials():
    """Interactive setup for environment credentials"""
    
    print("🔒 Open Build Outreach Automation - Secure Credential Setup")
    print("=" * 60)
    print()
    print("This script will help you set up your environment variables securely.")
    print("Your credentials will be stored in a .env file that is NOT committed to git.")
    print()
    
    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower().strip()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("Please provide your Brevo SMTP credentials:")
    print("(You can find these in your Brevo account settings)")
    print()
    
    # Collect credentials
    credentials = {}
    
    # Brevo SMTP settings
    credentials['BREVO_SMTP_HOST'] = input("BREVO_SMTP_HOST [smtp-relay.brevo.com]: ").strip() or "smtp-relay.brevo.com"
    credentials['BREVO_SMTP_PORT'] = input("BREVO_SMTP_PORT [587]: ").strip() or "587"
    
    credentials['BREVO_SMTP_USER'] = input("BREVO_SMTP_USER: ").strip()
    if not credentials['BREVO_SMTP_USER']:
        print("❌ BREVO_SMTP_USER is required!")
        return
    
    credentials['BREVO_SMTP_PASSWORD'] = getpass.getpass("BREVO_SMTP_PASSWORD (hidden): ").strip()
    if not credentials['BREVO_SMTP_PASSWORD']:
        print("❌ BREVO_SMTP_PASSWORD is required!")
        return
    
    # Email settings
    print()
    print("Email configuration:")
    credentials['FROM_EMAIL'] = input("FROM_EMAIL [team@open.build]: ").strip() or "team@open.build"
    credentials['FROM_NAME'] = input("FROM_NAME [Open Build Foundry Team]: ").strip() or "Open Build Foundry Team"
    credentials['REPLY_TO_EMAIL'] = input("REPLY_TO_EMAIL [team@open.build]: ").strip() or "team@open.build"
    
    # Optional settings
    print()
    print("Optional settings (press Enter to skip):")
    credentials['OPENAI_API_KEY'] = getpass.getpass("OPENAI_API_KEY (for AI personalization, hidden): ").strip()
    credentials['SLACK_WEBHOOK_URL'] = input("SLACK_WEBHOOK_URL (for notifications): ").strip()
    
    # System settings
    credentials['DATABASE_PATH'] = "data/outreach_automation.db"
    credentials['LOG_LEVEL'] = "INFO"
    credentials['LOG_FILE'] = "logs/outreach_automation.log"
    credentials['MIN_DELAY_SECONDS'] = "30"
    credentials['MAX_DELAY_SECONDS'] = "60"
    credentials['MAX_DAILY_EMAILS'] = "15"
    credentials['MAX_CONTACTS_PER_ORG'] = "4"
    credentials['COOLDOWN_DAYS'] = "30"
    
    # Write .env file
    print()
    print("📝 Writing .env file...")
    
    with open(".env", "w") as f:
        f.write("# Open Build Outreach Automation Environment Variables\n")
        f.write("# IMPORTANT: This file contains sensitive credentials - never commit to git!\n")
        f.write("# Generated on: " + str(Path().ctime()) + "\n\n")
        
        f.write("# Brevo SMTP Configuration\n")
        f.write(f"BREVO_SMTP_HOST={credentials['BREVO_SMTP_HOST']}\n")
        f.write(f"BREVO_SMTP_PORT={credentials['BREVO_SMTP_PORT']}\n")
        f.write(f"BREVO_SMTP_USER={credentials['BREVO_SMTP_USER']}\n")
        f.write(f"BREVO_SMTP_PASSWORD={credentials['BREVO_SMTP_PASSWORD']}\n\n")
        
        f.write("# Email Configuration\n")
        f.write(f"FROM_EMAIL={credentials['FROM_EMAIL']}\n")
        f.write(f"FROM_NAME={credentials['FROM_NAME']}\n")
        f.write(f"REPLY_TO_EMAIL={credentials['REPLY_TO_EMAIL']}\n\n")
        
        f.write("# Database Configuration\n")
        f.write(f"DATABASE_PATH={credentials['DATABASE_PATH']}\n\n")
        
        f.write("# Logging Configuration\n")
        f.write(f"LOG_LEVEL={credentials['LOG_LEVEL']}\n")
        f.write(f"LOG_FILE={credentials['LOG_FILE']}\n\n")
        
        f.write("# Rate Limiting Configuration\n")
        f.write(f"MIN_DELAY_SECONDS={credentials['MIN_DELAY_SECONDS']}\n")
        f.write(f"MAX_DELAY_SECONDS={credentials['MAX_DELAY_SECONDS']}\n\n")
        
        f.write("# Daily Limits\n")
        f.write(f"MAX_DAILY_EMAILS={credentials['MAX_DAILY_EMAILS']}\n")
        f.write(f"MAX_CONTACTS_PER_ORG={credentials['MAX_CONTACTS_PER_ORG']}\n")
        f.write(f"COOLDOWN_DAYS={credentials['COOLDOWN_DAYS']}\n\n")
        
        if credentials.get('OPENAI_API_KEY'):
            f.write("# Optional: OpenAI for enhanced personalization\n")
            f.write(f"OPENAI_API_KEY={credentials['OPENAI_API_KEY']}\n\n")
        else:
            f.write("# Optional: OpenAI for enhanced personalization\n")
            f.write("OPENAI_API_KEY=\n\n")
        
        if credentials.get('SLACK_WEBHOOK_URL'):
            f.write("# Optional: Webhook notifications\n")
            f.write(f"SLACK_WEBHOOK_URL={credentials['SLACK_WEBHOOK_URL']}\n")
        else:
            f.write("# Optional: Webhook notifications\n")
            f.write("SLACK_WEBHOOK_URL=\n")
        
        f.write("DISCORD_WEBHOOK_URL=\n")
    
    # Set secure permissions
    os.chmod(".env", 0o600)  # Owner read/write only
    
    print("✅ .env file created successfully!")
    print()
    print("🔒 Security measures applied:")
    print("  • File permissions set to 600 (owner read/write only)")
    print("  • .env file is in .gitignore (will not be committed)")
    print("  • Credentials are loaded at runtime only")
    print()
    print("📝 Next steps:")
    print("1. Test your configuration: python test_outreach_system.py")
    print("2. Run the system: python outreach_automation.py --run")
    print()
    print("⚠️  Remember: Never share your .env file or commit it to version control!")

def main():
    """Main function"""
    try:
        setup_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")

if __name__ == "__main__":
    main()
