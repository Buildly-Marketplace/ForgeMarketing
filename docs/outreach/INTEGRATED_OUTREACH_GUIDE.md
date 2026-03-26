# 🚀 Integrated Outreach Management Dashboard

## Overview

The outreach system has been fully integrated into your marketing dashboard, providing a complete web-based interface for managing email campaigns across all your brands. You can now upload CSV files, customize templates, preview emails, and send campaigns directly through the dashboard.

## 🎯 **Key Features**

### ✅ **Brand-Specific Configuration**
- **5 Brands Supported**: Buildly, Foundry, Open Build, Radical Therapy, Oregon Software
- **Custom Templates**: Each brand has tailored email templates
- **Brand Colors & Styling**: Consistent with each brand's identity
- **Targeting Options**: Segment users by account type, usage level, features used

### ✅ **Web-Based CSV Management**
- **Drag & Drop Upload**: Easy CSV file upload with preview
- **Flexible Field Mapping**: Automatically maps common CSV columns
- **Data Validation**: Preview your data before sending
- **Campaign Settings**: Set limits, skip recent contacts, test mode

### ✅ **Template System**
- **Pre-built Templates**: Account updates, feature announcements, re-engagement
- **Custom Templates**: Fully customizable subject and message
- **Dynamic Personalization**: Uses user data for personalized content
- **Preview Generation**: See exactly how emails will look

### ✅ **Safety & Control**
- **Preview Mode**: Always test before sending real emails
- **Rate Limiting**: Automatic delays to prevent spam flags
- **Opt-out Tracking**: Respects user unsubscribe preferences
- **Daily Limits**: Configurable sending limits per brand

### ✅ **Campaign Analytics**
- **Real-time Stats**: Track sent, failed, and skipped emails
- **Campaign History**: View all past campaigns
- **Performance Metrics**: Success rates and user engagement
- **Brand Analytics**: Separate tracking for each brand

## 🛠️ **How to Use**

### **Step 1: Access the Dashboard**
```bash
# Start the dashboard
cd "/Users/greglind/Projects/Sales and Marketing"
source .venv/bin/activate
python dashboard/app.py
```
**Dashboard URL**: http://localhost:5003

### **Step 2: Navigate to Outreach**
1. Open the dashboard in your browser
2. Click "Manage Outreach" from the main dashboard
3. Select your brand from the dropdown

### **Step 3: Upload Your CSV**
1. **Drag & drop** your CSV file or click "Browse Files"
2. **Preview the data** to ensure proper formatting
3. **Required column**: `email` (others are optional but helpful)

**Supported CSV Columns**:
```
email (required)     - User's email address
name                 - Full name
company              - Company/organization name  
account_type         - Free, Premium, Business, Enterprise
last_login           - Last login date (YYYY-MM-DD)
signup_date          - Account creation date
features_used        - Features or modules they use
subscription_status  - Active, Inactive, Trial, etc.
usage_level         - Low, Medium, High, Very High
custom_field_1      - Any custom data
custom_field_2      - Any custom data
```

### **Step 4: Choose Your Template**
Select from brand-specific templates:

**Buildly Templates**:
- Account Update
- Feature Announcement
- User Re-engagement
- API Updates
- Enterprise Outreach
- Custom Message

**Other Brands** have their own specialized templates for their industries.

### **Step 5: Configure Campaign**
- **Campaign Name**: Give your campaign a descriptive name
- **Max Emails**: Limit the number of emails (optional)
- **Skip Recent Contacts**: Avoid emailing users contacted recently
- **Test Mode**: Enable for preview-only campaigns

### **Step 6: Preview & Send**
1. **Generate Preview**: See how emails will look with real user data
2. **Validate Campaign**: Check for any issues
3. **Preview Campaign**: Run in test mode first
4. **Send Emails**: Execute the real campaign

## 📊 **Brand-Specific Features**

### **Buildly** 
- **Focus**: Developer tools and low-code platform
- **Templates**: Technical features, API updates, enterprise solutions
- **Targeting**: Developers, product managers, enterprises, startups

### **Foundry**
- **Focus**: Startup incubation and entrepreneur support  
- **Templates**: Startup outreach, investor updates, mentor recruitment
- **Targeting**: Startups, investors, mentors, media

### **Open Build**
- **Focus**: Open-source development community
- **Templates**: Community updates, project launches, contributor recognition
- **Targeting**: Developers, maintainers, companies, students

### **Radical Therapy**
- **Focus**: Mental health and wellness services
- **Templates**: Appointment reminders, wellness tips, method introduction
- **Targeting**: Clients, prospects, practitioners, advocates

### **Oregon Software**
- **Focus**: Custom software development services
- **Templates**: Consultation offers, case studies, technology insights
- **Targeting**: Prospects, existing clients, partners, developers

## 🔒 **Safety Features**

### **Built-in Protection**
- **Preview Mode**: All campaigns default to preview-only
- **Rate Limiting**: 5-15 second delays between emails
- **Daily Limits**: Maximum 200 emails per brand per day
- **Recent Contact Skip**: Avoid contacting users within 30 days
- **Opt-out Enforcement**: Automatic respect for unsubscribes

### **Best Practices**
1. **Always Preview First**: Use test mode before real sends
2. **Start Small**: Begin with max 10-50 emails for testing
3. **Segment Your Users**: Use different templates for different user types
4. **Monitor Results**: Check campaign analytics and logs
5. **Respect Limits**: Don't exceed daily sending limits

## 📈 **Analytics & Monitoring**

### **Campaign Tracking**
- **Real-time Stats**: See results as campaigns run
- **Success Rates**: Track delivery and failure rates
- **User Segmentation**: Analyze performance by user type
- **Historical Data**: Compare campaign performance over time

### **Log Files**
- **Detailed Logs**: `marketing/buildly_outreach_data/logs/`
- **Campaign History**: `marketing/buildly_outreach_data/outreach_log.json`
- **Opt-out List**: `marketing/buildly_outreach_data/opt_outs.json`

## 🛠️ **Configuration**

### **Email Credentials**
Set up your email settings in environment variables:
```bash
export BUILDLY_FROM_EMAIL="team@buildly.io"
export BUILDLY_EMAIL_PASSWORD="your-gmail-app-password"
export BUILDLY_SMTP_SERVER="smtp.gmail.com"
export BUILDLY_SMTP_PORT="587"
```

### **Brand Configuration**
Edit `/config/outreach_config.yaml` to:
- Add new templates
- Modify targeting segments
- Adjust rate limits
- Update brand settings

## 🚨 **Troubleshooting**

### **Common Issues**

**"Outreach system not available"**
- Ensure dependencies are installed: `pip install jinja2 yagmail`
- Check that the outreach script is accessible

**"CSV upload failed"**  
- Verify CSV has `email` column
- Check file encoding (should be UTF-8)
- Ensure proper CSV formatting

**"Email sending failed"**
- Verify email credentials are set correctly
- Check Gmail app password (not regular password)
- Ensure 2-factor authentication is enabled on Gmail

**"Preview not generating"**
- Check that brand is selected
- Verify template is chosen
- Ensure CSV data is loaded properly

### **Support**
- **Logs**: Check `marketing/buildly_outreach_data/logs/` for detailed error messages
- **Test Script**: Run `python test_outreach_dashboard.py` to verify system health
- **Dashboard Status**: Visit http://localhost:5003/api/status for system status

## 🎉 **Success!**

You now have a complete, integrated outreach management system that allows you to:

✅ **Upload CSV files** through a web interface  
✅ **Manage campaigns** for all 5 brands from one dashboard  
✅ **Customize templates** for each brand and use case  
✅ **Preview emails** before sending to ensure quality  
✅ **Track campaigns** with detailed analytics and logging  
✅ **Scale safely** with built-in limits and protection  

The system is production-ready and can handle your Buildly user outreach needs while providing the flexibility to expand to other brands as needed!

**Next Steps**: 
1. Upload your CSV file of Buildly users
2. Start with a small test campaign (10-20 users)
3. Review the results and adjust templates as needed
4. Scale up to full campaigns with confidence