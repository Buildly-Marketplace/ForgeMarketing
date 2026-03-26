#!/bin/bash

# Open Build Training Blog - Daily Article Generation and Publishing
# This script runs daily to generate new articles and update the blog

set -euo pipefail  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
BLOG_LOG="$LOG_DIR/blog_generation.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$DATE] $1" | tee -a "$BLOG_LOG"
}

# Error handling
handle_error() {
    local exit_code=$?
    log "ERROR: Blog generation failed with exit code $exit_code"
    
    # Send error notification email (using the environment variables)
    if command -v python3 >/dev/null; then
        python3 -c "
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

try:
    # Load environment
    exec(open('$PROJECT_DIR/.env').read().replace('export ', ''))
    
    # Email configuration
    smtp_host = os.getenv('BREVO_SMTP_HOST')
    smtp_port = int(os.getenv('BREVO_SMTP_PORT', 587))
    smtp_user = os.getenv('BREVO_SMTP_USER')
    smtp_password = os.getenv('BREVO_SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    team_email = os.getenv('TEAM_EMAIL')
    
    if all([smtp_host, smtp_user, smtp_password, from_email, team_email]):
        msg = MIMEText(f'''Blog generation failed at {datetime.now()}
        
Error details:
- Exit code: $exit_code
- Check logs: $BLOG_LOG
- Script: $0

Please investigate and resolve the issue.
''')
        msg['Subject'] = 'Open Build Blog Generation - FAILED'
        msg['From'] = from_email
        msg['To'] = team_email
        
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print('Error notification sent')
    else:
        print('Email configuration incomplete - notification not sent')
        
except Exception as e:
    print(f'Failed to send error notification: {e}')
"
    fi
    
    exit $exit_code
}

# Set up error handling
trap 'handle_error' ERR

# Main execution
main() {
    log "=== Open Build Blog Generation Started ==="
    
    # Change to project directory
    cd "$PROJECT_DIR" || {
        log "ERROR: Cannot change to project directory: $PROJECT_DIR"
        exit 1
    }
    
    # Load environment variables
    if [[ -f ".env" ]]; then
        log "Loading environment variables..."
        set -o allexport
        # Use export syntax to handle spaces in values
        eval "$(grep -v '^#' .env | grep -v '^$' | sed 's/^/export /')"
        set +o allexport
    else
        log "WARNING: .env file not found"
    fi
    
    # Check if blog generation is enabled
    if [[ "${BLOG_ENABLED:-true}" != "true" ]]; then
        log "Blog generation is disabled - skipping"
        exit 0
    fi
    
    # Check Python availability
    if ! command -v python3 >/dev/null; then
        log "ERROR: Python 3 not found"
        exit 1
    fi
    
    # Check Ollama service availability
    log "Checking Ollama service..."
    ollama_host="${OLLAMA_HOST:-http://pop-os2.local:11434}"
    
    if curl -s -f "${ollama_host}/api/version" >/dev/null 2>&1; then
        log "Ollama service is available"
    else
        log "WARNING: Ollama service not available - articles may not generate"
    fi
    
    # Generate today's blog article
    log "Generating daily blog article..."
    if python3 scripts/blog_generator.py --generate; then
        log "Blog article generated successfully"
    else
        log "WARNING: Blog article generation failed"
    fi
    
    # Update blog index page with new article
    log "Updating blog index page..."
    if python3 scripts/update_blog_index.py; then
        log "Blog index updated successfully"
    else
        log "WARNING: Blog index update failed"
    fi
    
    # Optional: Commit and push to git (if this is a git repository)
    if [[ -d ".git" ]] && [[ "${GIT_AUTO_COMMIT:-false}" == "true" ]]; then
        log "Auto-committing blog updates to git..."
        
        git add blog/ training-blog.html 2>/dev/null || true
        
        if git diff --cached --quiet; then
            log "No changes to commit"
        else
            git commit -m "Automated blog update - $(date '+%Y-%m-%d')" || {
                log "WARNING: Git commit failed"
            }
            
            # Push if configured
            if [[ "${GIT_AUTO_PUSH:-false}" == "true" ]]; then
                git push origin main 2>/dev/null || {
                    log "WARNING: Git push failed"
                }
            fi
        fi
    fi
    
    log "=== Blog Generation Completed Successfully ==="
}

# Run main function
main "$@"