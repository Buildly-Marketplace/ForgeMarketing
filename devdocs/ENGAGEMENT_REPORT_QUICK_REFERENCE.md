# Email Engagement Report - Quick Reference Guide

## 🚀 Quick Start

### Access the Report
```
http://localhost:8002/engagement-report
```

### Navigation
- Click **"📧 Engagement Report"** in the sidebar
- Or navigate via main menu

---

## 📊 Report Sections

### 1. Summary Cards (Top)
Shows aggregated metrics across all brands:
- **Emails Sent**: Total emails sent in period
- **Delivered**: How many actually reached inboxes
- **Opened**: How many were opened by recipients
- **Clicked**: How many had link clicks

### 2. Performance by Brand Table
Compares all 5 brands side-by-side:
- **Brand**: Company name
- **Sent**: Total emails sent
- **Delivered**: Successfully delivered
- **Opens**: Number of opens
- **Open Rate**: Percentage who opened (%)
- **Clicks**: Number of link clicks
- **Click Rate**: Percentage who clicked (%)
- **Campaigns**: How many campaigns sent
- **Action**: "View" button for drill-down

### 3. Brand Detail Modal
Click "View" on any brand row to see:
- Summary stats for that brand
- List of all campaigns sent
- Campaign subject lines
- Send dates and performance metrics
- Campaign-level open/click rates

### 4. Campaign Detail Modal
Click on any campaign to see:
- Campaign name and subject
- Send date and status
- Metrics grid showing:
  - Sent vs. Delivered counts
  - Delivery rate %
  - Opens and open rate %
  - Clicks and click rate %
  - Bounces and bounce rate %
  - Unsubscribes and rate %
- Recipient engagement summary

---

## 🎯 Common Tasks

### View Email Performance for a Brand
1. Open engagement report
2. Scroll to "Performance by Brand" table
3. Find brand in list (Buildly, Foundry, OpenBuild, Radical, Oregon Software)
4. Check metrics (sent, open rate, click rate)
5. Click "View" to see individual campaigns

### See Individual Campaign Performance
1. Click "View" on any brand
2. Brand detail modal opens
3. See list of campaigns
4. Click on a campaign to view detailed metrics

### Compare All Brands
1. Look at "Performance by Brand" table
2. Compare columns:
   - Sent: Who sent most emails?
   - Open Rate: Who has best engagement?
   - Click Rate: Who drives most clicks?

### Export Data for Analysis
1. Click "Export" button (top right)
2. CSV file downloads automatically
3. Open in Excel/Google Sheets
4. Analyze further if needed

### Refresh Data
1. Click "Refresh" button (top right)
2. Data re-fetches from email provider
3. Shows latest metrics

### Filter by Time Period
1. Change dropdown (top right):
   - "Last 7 days"
   - "Last 30 days" (default)
   - "Last 90 days"
2. Metrics update automatically

---

## 📈 Understanding the Metrics

### Delivery Rate
```
(Delivered / Sent) × 100 = Delivery Rate %
Example: 2,375 / 2,500 × 100 = 95%
```
**What it means**: How many emails actually reached inboxes
**Good rate**: 95%+ (some bounces/blocks are normal)

### Open Rate
```
(Opens / Delivered) × 100 = Open Rate %
Example: 522 / 2,375 × 100 = 22%
```
**What it means**: What % of delivered emails were opened
**Good rate**: 15-25% (depends on industry)

### Click Rate
```
(Clicks / Opens) × 100 = Click Rate %
Example: 83 / 522 × 100 = 15.9%
```
**What it means**: What % of people who opened clicked a link
**Good rate**: 5-15% (varies by content)

### Bounce Rate
```
(Bounces / Sent) × 100 = Bounce Rate %
Example: 50 / 2,500 × 100 = 2%
```
**What it means**: % of emails that couldn't be delivered
**Good rate**: Under 3% (indicates clean list)

### Unsubscribe Rate
```
(Unsubscribes / Sent) × 100 = Unsubscribe Rate %
Example: 12 / 2,500 × 100 = 0.48%
```
**What it means**: % of recipients who unsubscribed
**Good rate**: Under 1% (indicates quality content)

---

## 🔍 Sample Data

### Summary Stats (All Brands)
- Total Sent: 10,700
- Total Delivered: 10,165
- Total Opened: 2,234
- Total Clicked: 353
- Avg Open Rate: 22%
- Avg Click Rate: 3.5%

### By Brand Example (Buildly)
- Sent: 2,500
- Delivered: 2,375
- Delivered Rate: 95%
- Open Rate: 22%
- Click Rate: 3.5%
- Bounces: 50
- Unsubscribes: 12
- Campaigns: 2

### Campaign Example (Weekly Newsletter)
- Status: Sent
- Sent Date: [date]
- Sent: 1,000
- Delivered: 950
- Delivery Rate: 95%
- Opens: 209
- Open Rate: 22%
- Clicks: 35
- Click Rate: 3.7%
- Bounces: 20
- Bounce Rate: 2%
- Unsubscribes: 5
- Unsubscribe Rate: 0.5%

---

## ⚙️ Configuration

### Current Status
- System shows **MOCK DATA** (for testing/demo)
- Mock data is realistic and based on typical email metrics

### Enable Real Email Provider Data

**For Brevo (Sendinblue):**

1. Get API Key from Brevo:
   - Log in to https://www.brevo.com
   - Settings → SMTP & API
   - Copy API Key

2. Add to `.env` file:
   ```
   BUILDLY_EMAIL_API_KEY=xxxxxxxxxxx
   FOUNDRY_EMAIL_API_KEY=xxxxxxxxxxx
   OPENBUILD_EMAIL_API_KEY=xxxxxxxxxxx
   RADICAL_EMAIL_API_KEY=xxxxxxxxxxx
   OREGONSOFTWARE_EMAIL_API_KEY=xxxxxxxxxxx
   ```

3. Restart server:
   ```bash
   ./ops/startup.sh restart
   ```

4. Engagement report will now show **REAL** email data!

---

## 🔗 API Reference

### Get Summary Data
```bash
curl "http://localhost:8002/api/engagement/email-summary?days=30"
```
Returns: Total metrics across all brands

### Get Brand Details
```bash
curl "http://localhost:8002/api/engagement/brand-detail/buildly?days=30"
```
Returns: All campaigns for specific brand

### Get Campaign Details
```bash
curl "http://localhost:8002/api/engagement/campaign/1?brand=buildly"
```
Returns: Individual campaign metrics

---

## 🆘 Troubleshooting

### Seeing "Mock Data" instead of Real Data
**Solution**: 
1. Configure email provider API keys in `.env`
2. Restart server
3. Refresh engagement report

### No Data Appearing
**Solution**:
1. Check that server is running: `curl http://localhost:8002/`
2. Check API is working: `curl http://localhost:8002/api/engagement/email-summary`
3. Refresh page (Ctrl+R or Cmd+R)

### Export Not Working
**Solution**:
1. Make sure you have CSV data first
2. Try different browser if needed
3. Check browser download folder

### Drill-Down Modal Not Opening
**Solution**:
1. Make sure JavaScript is enabled
2. Try refreshing page
3. Try different browser
4. Check browser console for errors (F12)

---

## 📚 Further Documentation

For detailed technical documentation:
```
/ENGAGEMENT_REPORT_IMPLEMENTATION.md
```

This contains:
- Architecture overview
- API endpoint details
- Data structure specifications
- Configuration instructions
- Integration guides

---

## 🎯 Best Practices

### Viewing Performance
1. **Start with summary**: See overall trends first
2. **Then compare brands**: Find underperformers
3. **Drill into campaigns**: See what worked best
4. **Export and analyze**: Use data for strategy

### Interpreting Results
- **Low open rates?** Subject lines may need improvement
- **Low click rates?** Content may not be compelling
- **High bounce rates?** Email list needs cleaning
- **High unsubscribes?** Check email frequency/quality

### Regular Monitoring
- Check report weekly
- Look for trend changes
- Compare week-over-week/month-over-month
- Use insights to improve campaigns

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review technical documentation
3. Check server logs: `/logs/`
4. Verify email provider API keys in `.env`

---

Last Updated: November 15, 2025
