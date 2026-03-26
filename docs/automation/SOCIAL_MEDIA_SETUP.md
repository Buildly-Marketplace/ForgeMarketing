# Social Media Platform Integration Guide

## Overview
This guide covers the OAuth2 and API token setup required for each social media platform integration. The dashboard supports Twitter/X, BlueSky, Instagram, and LinkedIn with real-time posting and analytics.

## Current Status
- ✅ **Blog Integration**: Fully working - tracks local blog generation
- 🔧 **Social Media APIs**: Framework ready, requires API credentials
- 📊 **Analytics**: Real-time data collection implemented
- 🤖 **AI Integration**: Working with Ollama for content generation

---

## 1. Twitter/X API Setup

### Requirements
- Twitter Developer Account
- Elevated access for posting tweets
- OAuth 1.0a credentials

### Setup Steps
1. **Apply for Developer Account**
   - Go to [developer.twitter.com](https://developer.twitter.com/)
   - Apply for developer access (may take 1-3 days)
   - Create a new "App" in the developer portal

2. **Generate API Keys**
   - API Key and Secret (Consumer Key/Secret)
   - Access Token and Secret
   - Bearer Token (for API v2 read operations)

3. **Set Environment Variables**
   ```bash
   export TWITTER_API_KEY="your_api_key"
   export TWITTER_API_SECRET="your_api_secret"
   export TWITTER_ACCESS_TOKEN="your_access_token"
   export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
   export TWITTER_BEARER_TOKEN="your_bearer_token"
   ```

### Permissions Needed
- Read and Write permissions
- Direct message permissions (optional)

### Rate Limits
- 300 tweets per 15-minute window
- 900 API calls per 15-minute window

---

## 2. BlueSky Integration

### Requirements
- BlueSky account
- App password (not your main password)

### Setup Steps
1. **Create App Password**
   - Go to BlueSky Settings > App Passwords
   - Generate a new app password
   - Save the password securely

2. **Set Environment Variables**
   ```bash
   export BLUESKY_USERNAME="your.handle.bsky.social"
   export BLUESKY_APP_PASSWORD="your_app_password"
   ```

### API Details
- Uses AT Protocol (ATP)
- No OAuth required - uses username/app-password auth
- Endpoint: `https://bsky.social/xrpc`

### Rate Limits
- 300 posts per day
- 10,000 reads per hour

---

## 3. Instagram Business API

### Requirements
- Instagram Business Account
- Facebook Developer Account
- Facebook App with Instagram permissions

### Setup Steps
1. **Convert to Business Account**
   - Switch your Instagram account to Business
   - Connect to a Facebook Page

2. **Create Facebook App**
   - Go to [developers.facebook.com](https://developers.facebook.com/)
   - Create new app, select "Business"
   - Add Instagram Graph API product

3. **Get Access Tokens**
   - Generate User Access Token
   - Exchange for Long-Lived Token (60 days)
   - Optionally create Page Access Token

4. **Set Environment Variables**
   ```bash
   export INSTAGRAM_APP_ID="your_app_id"
   export INSTAGRAM_APP_SECRET="your_app_secret"
   export INSTAGRAM_ACCESS_TOKEN="your_long_lived_token"
   ```

### Permissions Required
- `instagram_graph_user_profile`
- `instagram_graph_user_media`
- `pages_show_list` (if using page tokens)

### Important Notes
- **Requires Media**: Instagram posts must include images or videos
- **Business Only**: Personal accounts cannot use the API
- Review process required for production use

### Rate Limits
- 25 posts per day per user
- 200 API calls per hour

---

## 4. LinkedIn API

### Requirements
- LinkedIn Developer Account
- Company Page (for organization posts)
- App approval for posting permissions

### Setup Steps
1. **Create LinkedIn App**
   - Go to [developer.linkedin.com](https://developer.linkedin.com/)
   - Create new app
   - Verify company association

2. **OAuth 2.0 Flow**
   - Redirect users to LinkedIn authorization
   - Exchange authorization code for access token
   - Refresh tokens as needed

3. **Set Environment Variables**
   ```bash
   export LINKEDIN_CLIENT_ID="your_client_id"
   export LINKEDIN_CLIENT_SECRET="your_client_secret"
   export LINKEDIN_ACCESS_TOKEN="your_access_token"
   export LINKEDIN_REFRESH_TOKEN="your_refresh_token"
   ```

### Scopes Required
- `w_member_social`: Post updates
- `r_liteprofile`: Read profile info
- `r_organization_social`: Post to company pages

### Rate Limits
- 100 posts per day per user
- 500 API calls per day

---

## 5. Environment Configuration

### Development Setup
Create a `.env` file in your project root:
```bash
# Twitter/X
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# BlueSky
BLUESKY_USERNAME=your.handle.bsky.social
BLUESKY_APP_PASSWORD=your_app_password

# Instagram
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_ACCESS_TOKEN=your_access_token

# LinkedIn
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_REFRESH_TOKEN=your_refresh_token
```

### Production Setup
Use environment variables or a secure secrets manager:
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Kubernetes secrets

---

## 6. Testing the Integration

### Check Current Status
1. Open the dashboard at `http://localhost:5001`
2. Go to Settings > AI Configuration
3. Use "Test AI Connection" to verify AI is working
4. Check Analytics page for real activity data

### Test Social Media Posting
1. Go to Content Generation page
2. Select a brand and platform
3. Generate content with AI
4. Post to configured platforms

### Monitor Activity
- Analytics page shows real-time social media activity
- Blog posts are automatically detected from local generation
- Performance metrics update based on actual posting activity

---

## 7. Security Best Practices

### Token Management
- Never commit credentials to version control
- Use environment variables or secure storage
- Rotate tokens regularly
- Monitor API usage for unusual activity

### Access Control
- Use least-privilege principle
- Separate tokens for different environments
- Monitor and audit API access
- Set up alerts for rate limit breaches

### Data Privacy
- Comply with platform policies
- Respect user privacy
- Handle personal data appropriately
- Maintain audit logs

---

## 8. Current Implementation Status

### ✅ Working Features
- **AI Content Generation**: Ollama integration working
- **Blog Detection**: Automatically finds generated blog posts
- **Dashboard UI**: All pages functional
- **Configuration System**: Productized config management
- **Analytics Framework**: Real-time data collection ready

### 🔧 Requires API Keys
- **Twitter Posting**: Framework ready, needs credentials
- **BlueSky Posting**: Framework ready, needs credentials  
- **Instagram Posting**: Framework ready, needs credentials + media
- **LinkedIn Posting**: Framework ready, needs credentials

### 📋 Next Steps
1. **Set up API credentials** for desired platforms
2. **Test posting functionality** with real credentials
3. **Configure platform-specific content adaptation**
4. **Set up automated cross-posting schedules**
5. **Monitor and optimize posting times**

---

## 9. Troubleshooting

### Common Issues
1. **Rate Limiting**: Implement backoff strategies
2. **Token Expiration**: Set up automatic refresh
3. **Content Rejection**: Check platform policies
4. **API Changes**: Monitor platform documentation

### Debug Mode
Enable debug logging in the dashboard settings:
```python
# In dashboard/app.py
app.config['DEBUG'] = True
logging.getLogger().setLevel(logging.DEBUG)
```

### Log Files
Check these locations for debugging:
- `/logs/social_media.log` - Social media integration logs
- `/logs/dashboard.log` - Dashboard application logs
- `/logs/ai_integration.log` - AI generation logs

---

## Support Resources

- **Twitter API Docs**: [developer.twitter.com/en/docs](https://developer.twitter.com/en/docs)
- **BlueSky AT Protocol**: [atproto.com](https://atproto.com)
- **Instagram Graph API**: [developers.facebook.com/docs/instagram-api](https://developers.facebook.com/docs/instagram-api)
- **LinkedIn API Docs**: [docs.microsoft.com/en-us/linkedin](https://docs.microsoft.com/en-us/linkedin)

For technical issues with this integration, check the project documentation or open an issue in the repository.