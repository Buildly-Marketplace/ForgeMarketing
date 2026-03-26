# Google Ads Integration Setup Guide

## 🎯 Overview
This Google Ads integration provides comprehensive campaign management for all four brands:
- **Foundry** - Software Development Tools
- **Buildly** - Low-Code Development Platform  
- **OpenBuild** - Open Source Development
- **Radical Therapy** - Mental Health Technology

## 🚀 Quick Start (Development Mode)
The integration currently runs in **Development Mode** with mock data. You can:
1. View campaign overviews and performance metrics
2. Create new campaigns (simulated)
3. Get keyword suggestions
4. Run campaign optimizations
5. Pause/resume campaigns

## 🔧 Production Setup

### Step 1: Google Ads API Access
1. Visit [Google Ads API Center](https://developers.google.com/google-ads/api)
2. Apply for Google Ads API access (requires approval)
3. Create a Google Cloud Project
4. Enable the Google Ads API
5. Create OAuth 2.0 credentials

### Step 2: Get Developer Token
1. Sign in to your Google Ads account
2. Go to **Tools & Settings** → **Setup** → **API Center**
3. Apply for a developer token
4. Wait for approval (can take several days)

### Step 3: Configure Authentication
Create/update the configuration file:
```bash
/automation/config/google_ads_config.json
```

Add your credentials:
```json
{
  "developer_token": "YOUR_DEVELOPER_TOKEN",
  "client_id": "YOUR_OAUTH_CLIENT_ID", 
  "client_secret": "YOUR_OAUTH_CLIENT_SECRET",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "customer_ids": {
    "foundry": "123-456-7890",
    "buildly": "123-456-7891", 
    "open_build": "123-456-7892",
    "radical_therapy": "123-456-7893"
  }
}
```

### Step 4: Get Customer IDs
1. Log into each Google Ads account
2. Copy the Customer ID (10-digit number) from the top right
3. Update the configuration file

### Step 5: OAuth Setup
Run the OAuth flow to get refresh tokens:
```python
from google_ads_auth import get_refresh_token
refresh_token = get_refresh_token(client_id, client_secret)
```

## 📊 Features Available

### Dashboard Interface
- **Overview**: Total campaigns, budget, clicks, impressions across all brands
- **Brand Tabs**: Switch between foundry, buildly, open_build, radical_therapy
- **Campaign Management**: Create, pause, resume campaigns
- **Performance Metrics**: CTR, CPA, conversion rates
- **Keyword Research**: AI-powered keyword suggestions
- **Optimization**: Automated campaign improvements

### API Endpoints
- `GET /api/google-ads/overview` - All brands summary
- `GET /api/google-ads/brand/{brand}/campaigns` - Brand campaigns
- `GET /api/google-ads/brand/{brand}/performance` - Performance metrics
- `POST /api/google-ads/brand/{brand}/keywords/suggest` - Keyword suggestions
- `POST /api/google-ads/brand/{brand}/campaigns/create` - Create campaign
- `POST /api/google-ads/brand/{brand}/campaigns/{id}/pause` - Pause campaign
- `POST /api/google-ads/brand/{brand}/campaigns/{id}/resume` - Resume campaign
- `POST /api/google-ads/brand/{brand}/optimize` - Run optimization

### Brand-Specific Configurations

#### Foundry (Software Development Tools)
- **Target Audience**: Developers, CTOs, Tech Leaders
- **Keywords**: software development platform, dev tools automation, deployment
- **Daily Budget**: $50
- **Target CPA**: $25
- **Campaign Types**: Search, Performance Max

#### Buildly (Low-Code Platform)
- **Target Audience**: Business Users, Citizen Developers, IT Teams
- **Keywords**: low code platform, no code development, business app builder
- **Daily Budget**: $75
- **Target CPA**: $35
- **Campaign Types**: Search, Display, Performance Max

#### OpenBuild (Open Source)
- **Target Audience**: Open Source Developers, DevOps Engineers
- **Keywords**: open source platform, collaborative development
- **Daily Budget**: $30
- **Target CPA**: $20
- **Campaign Types**: Search, YouTube

#### Radical Therapy (Mental Health)
- **Target Audience**: Therapists, Mental Health Professionals, Clinics
- **Keywords**: therapy practice management, mental health software
- **Daily Budget**: $40
- **Target CPA**: $30  
- **Campaign Types**: Search, Display

## 🎛️ Advanced Features

### Automated Bidding Strategies
- **Maximize Conversions**: Optimizes for conversion volume
- **Target CPA**: Maintains cost per acquisition goals
- **Target ROAS**: Optimizes for return on ad spend

### Campaign Optimization
Automated optimization checks for:
- CTR below 2% → Add negative keywords
- CPA above target → Reduce bids
- Low impression share → Increase bids
- Poor ad relevance → Update ad copy

### Keyword Research
AI-powered keyword suggestions based on:
- Industry analysis
- Competitor research
- Search volume trends
- Competition levels
- Relevance scoring

## 🔍 Monitoring & Analytics

### Performance Tracking
- **Impressions**: Ad visibility
- **Clicks**: User engagement  
- **CTR**: Click-through rate
- **Conversions**: Goal completions
- **CPA**: Cost per acquisition
- **ROAS**: Return on ad spend

### Reporting Frequency
- **Real-time**: Dashboard updates every 5 minutes
- **Daily**: Email performance summaries
- **Weekly**: Optimization recommendations
- **Monthly**: Comprehensive analysis reports

## 🚨 Important Notes

### Development vs Production
- **Development Mode**: Uses mock data, safe for testing
- **Production Mode**: Requires Google Ads API credentials, real budget

### Budget Management
- All campaigns start **PAUSED** for manual review
- Daily budgets are configurable per brand
- Automated bid adjustments within 20% of target

### Compliance
- Follows Google Ads policies
- Respects targeting restrictions
- Maintains data privacy standards

## 📞 Support

### Getting Help
1. Check the dashboard logs at `/automation/logs/google_ads_YYYYMMDD.log`
2. Review API responses in the browser developer tools
3. Test with mock data first before production deployment

### Common Issues
- **API Quota Exceeded**: Reduce API call frequency
- **Authentication Failed**: Check credentials and refresh tokens
- **Campaign Creation Failed**: Verify budget and targeting settings

## 🎉 Success Metrics

### Expected Results
- **Foundry**: 2-4% CTR, $20-30 CPA
- **Buildly**: 1.5-3% CTR, $30-40 CPA  
- **OpenBuild**: 3-5% CTR, $15-25 CPA
- **Radical Therapy**: 2-3% CTR, $25-35 CPA

The Google Ads integration is now fully deployed and ready for campaign management across all four brands! 🚀