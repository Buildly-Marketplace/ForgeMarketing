#!/bin/bash

# Open Build Outreach Automation Setup Script
# This script sets up the outreach automation system

echo "🚀 Setting up Open Build Outreach Automation System..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv outreach_env
source outreach_env/bin/activate

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Create data directory
mkdir -p data
mkdir -p logs

# Set up environment variables
echo "Setting up environment file..."
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "⚠️  IMPORTANT: Edit .env file with your actual Brevo SMTP credentials!"
    echo "⚠️  Your credentials should be added to the .env file manually."
else
    echo "✅ .env file already exists"
fi

# Database
DATABASE_PATH=data/outreach_automation.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/outreach_automation.log

# Rate Limiting
MIN_DELAY_SECONDS=30
MAX_DELAY_SECONDS=60

# Daily Limits
MAX_DAILY_EMAILS=15
MAX_CONTACTS_PER_ORG=4
COOLDOWN_DAYS=30

# Optional: OpenAI for enhanced personalization
OPENAI_API_KEY=your_openai_api_key_here
EOL

# Create systemd service file (Linux) or launchd plist (macOS)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Creating systemd service..."
    sudo cat > /etc/systemd/system/openbuild-outreach.service << EOL
[Unit]
Description=Open Build Outreach Automation
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/outreach_env/bin
ExecStart=$(pwd)/outreach_env/bin/python outreach_automation.py --run
Restart=daily
RestartSec=3600

[Install]
WantedBy=multi-user.target
EOL
    
    sudo systemctl daemon-reload
    echo "To enable daily automation: sudo systemctl enable openbuild-outreach.service"
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Creating macOS launch agent..."
    mkdir -p ~/Library/LaunchAgents
    cat > ~/Library/LaunchAgents/com.openbuild.outreach.plist << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openbuild.outreach</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(pwd)/outreach_env/bin/python</string>
        <string>$(pwd)/outreach_automation.py</string>
        <string>--run</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$(pwd)</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$(pwd)/logs/outreach_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$(pwd)/logs/outreach_stderr.log</string>
</dict>
</plist>
EOL
    echo "To enable daily automation: launchctl load ~/Library/LaunchAgents/com.openbuild.outreach.plist"
fi

# Make the main script executable
chmod +x outreach_automation.py

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your Brevo SMTP credentials"
echo "2. Verify environment variables: python test_outreach_system.py"
echo "3. Test the system: python outreach_automation.py --report"
echo "4. Run manual test: python outreach_automation.py --run"
echo "5. Enable daily automation using the commands shown above"
echo ""
echo "📖 Documentation:"
echo "• Environment variables: Configure in .env file (never commit this file!)"
echo "• Rate limiting: 30-60 seconds between requests"
echo "• Daily limit: 15 emails per day maximum"
echo "• Cooldown: 30 days between repeat contacts"
echo ""
echo "🎯 Ready to start building your outreach pipeline!"
