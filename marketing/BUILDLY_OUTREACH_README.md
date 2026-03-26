# Buildly User Outreach System

## Overview

The Buildly User Outreach System is a powerful tool for sending personalized emails to your Buildly users based on CSV data. It includes built-in templates for common scenarios and supports custom messaging.

## Features

- **CSV Processing**: Load user data from CSV files with flexible field mapping
- **Multiple Templates**: Pre-built templates for account updates, feature announcements, and re-engagement
- **Personalization**: Dynamic content based on user data (name, company, usage patterns, etc.)
- **Safety Features**: 
  - Preview mode to test emails before sending
  - Opt-out tracking and enforcement
  - Rate limiting to prevent spam
  - Daily sending limits
  - Recent contact tracking

## Setup

### 1. Install Dependencies

```bash
cd "/Users/greglind/Projects/Sales and Marketing"
source .venv/bin/activate
pip install jinja2 yagmail beautifulsoup4
```

### 2. Configure Email Settings

Set up your email credentials using environment variables:

```bash
# For Gmail (recommended for testing)
export BUILDLY_FROM_EMAIL="your-email@gmail.com"
export BUILDLY_EMAIL_PASSWORD="your-app-password"  # Use app password, not regular password
export BUILDLY_SMTP_SERVER="smtp.gmail.com"
export BUILDLY_SMTP_PORT="587"

# Optional settings
export BUILDLY_DAILY_EMAIL_LIMIT="100"  # Max emails per day
```

**Gmail Setup**: 
1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" in Google Account settings
3. Use the app password (not your regular password) in BUILDLY_EMAIL_PASSWORD

### 3. Prepare Your CSV File

Your CSV should include these columns (all are optional except email):

- `email` (required): User's email address
- `name`: Full name of the user
- `company`: Company/organization name
- `account_type`: Plan type (Free, Premium, Business, Enterprise)
- `last_login`: Last login date (YYYY-MM-DD format)
- `signup_date`: Account creation date
- `features_used`: Features or modules they use
- `subscription_status`: Active, Inactive, Trial, etc.
- `usage_level`: Low, Medium, High, Very High
- `custom_field_1`: Any custom data (e.g., "VIP Customer")
- `custom_field_2`: Any custom data (e.g., "Needs Follow-up")

**Note**: Column names are flexible. The system will map common variations:
- `full_name` → `name`
- `organization` → `company`
- `plan` → `account_type`
- `last_active` → `last_login`
- `created_at` → `signup_date`
- etc.

## Available Templates

### 1. Account Update (`account_update`)
General account updates and important announcements.

### 2. Feature Announcement (`feature_announcement`)  
Introducing new features and capabilities.

### 3. Re-engagement (`reengagement`)
For users who haven't been active recently. Includes special offers.

### 4. Custom (`custom`)
Fully customizable template where you provide the subject and message.

## Usage Examples

### Preview Emails (Safe Testing)

```bash
# Preview account update emails
python marketing/buildly_user_outreach.py \
    --csv your_users.csv \
    --template account_update \
    --preview

# Preview feature announcement for first 5 users
python marketing/buildly_user_outreach.py \
    --csv your_users.csv \
    --template feature_announcement \
    --preview \
    --max-emails 5

# Preview custom message
python marketing/buildly_user_outreach.py \
    --csv your_users.csv \
    --template custom \
    --custom-subject "Important: Update your payment method" \
    --custom-message "We need to update your payment information. Please log in to update your billing details." \
    --preview
```

### Send Real Emails

⚠️ **Warning**: Remove `--preview` only when you're ready to send real emails!

```bash
# Send account updates to all users
python marketing/buildly_user_outreach.py \
    --csv your_users.csv \
    --template account_update \
    --send

# Send feature announcements, max 50 emails
python marketing/buildly_user_outreach.py \
    --csv your_users.csv \
    --template feature_announcement \
    --send \
    --max-emails 50

# Include users contacted recently (normally skipped)
python marketing/buildly_user_outreach.py \
    --csv your_users.csv \
    --template reengagement \
    --send \
    --include-recent
```

## Safety Features

### 1. Preview Mode
Always test with `--preview` first to see exactly what will be sent.

### 2. Recent Contact Protection
By default, users contacted in the last 30 days are skipped. Use `--include-recent` to override.

### 3. Daily Limits
Default limit is 100 emails per day. Adjust with `BUILDLY_DAILY_EMAIL_LIMIT`.

### 4. Rate Limiting
5-15 second delays between emails to avoid being marked as spam.

### 5. Opt-out Tracking
Users who unsubscribe are automatically tracked and skipped in future campaigns.

## Monitoring and Logs

### Campaign Reports
Each campaign prints a detailed summary:
- Total users processed
- Emails sent/failed
- Users skipped (opt-outs, recent contacts, etc.)

### Detailed Logs
- `buildly_outreach_data/logs/`: Daily log files with detailed information
- `buildly_outreach_data/outreach_log.json`: Complete history of all sent emails
- `buildly_outreach_data/opt_outs.json`: List of users who have unsubscribed

### Analytics
Track campaign performance over time:
- Open rates (if using advanced email service)
- Response tracking
- User engagement patterns

## Best Practices

### 1. Start Small
Begin with `--max-emails 10` and `--preview` to test everything works.

### 2. Segment Your Users
Create separate CSV files for different user types:
- Active users: Feature announcements
- Inactive users: Re-engagement campaigns
- Enterprise users: Premium feature updates

### 3. Time Your Campaigns
- Send during business hours in your users' time zones
- Avoid Mondays and Fridays
- Space campaigns at least 1-2 weeks apart

### 4. Personalize Content
Use the custom fields to add specific information:
- Reference their company name
- Mention features they actually use
- Acknowledge their subscription level

### 5. Monitor Results
- Check logs for failed sends
- Watch for bounces and complaints
- Adjust messaging based on engagement

## Troubleshooting

### Email Not Sending
1. Check your environment variables are set correctly
2. Verify Gmail app password is correct
3. Check the logs for specific error messages

### Template Errors
1. Make sure CSV columns exist
2. Check for special characters in custom messages
3. Verify template name is spelled correctly

### Rate Limiting
If you're hitting limits:
1. Reduce daily limit
2. Increase delay between emails
3. Split large campaigns across multiple days

## Example Workflow

```bash
# 1. Test with sample data
python marketing/buildly_user_outreach.py \
    --csv marketing/example_users.csv \
    --template account_update \
    --preview

# 2. Test with your real data (small batch)
python marketing/buildly_user_outreach.py \
    --csv your_actual_users.csv \
    --template account_update \
    --preview \
    --max-emails 5

# 3. Send to small test group
python marketing/buildly_user_outreach.py \
    --csv your_test_users.csv \
    --template account_update \
    --send \
    --max-emails 10

# 4. Full campaign
python marketing/buildly_user_outreach.py \
    --csv your_actual_users.csv \
    --template account_update \
    --send
```

This system gives you powerful, safe email outreach capabilities while protecting your users and your reputation. Start small, test thoroughly, and scale up gradually!