# Reference

API endpoints, configuration options, and system architecture reference.

## Core API Endpoints

### Health & Status

```
GET /health
```

Returns system health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-14T12:00:00Z"
}
```

### Brands

```
GET /api/brands
```

List all configured brands.

```
GET /api/brands/{slug}
GET /api/brands/{slug}/config
```

Get brand configuration and settings.

### Campaigns

```
POST /api/campaigns
GET /api/campaigns
GET /api/campaigns/{id}
PUT /api/campaigns/{id}
DELETE /api/campaigns/{id}
```

Manage marketing campaigns.

### Content Generation

```
POST /api/content/generate
```

Generate content using AI models.

**Request:**
```json
{
  "brand_slug": "buildly",
  "content_type": "social_post",
  "topic": "AI automation",
  "style": "professional"
}
```

**Response:**
```json
{
  "id": "uuid",
  "content": "Generated content text...",
  "model": "mistral",
  "timestamp": "2025-11-14T12:00:00Z"
}
```

### Email Campaigns

```
POST /api/emails/send
GET /api/emails/stats
GET /api/emails/{campaign_id}/deliveries
```

Send emails and track delivery.

### Analytics

```
GET /api/analytics/dashboard
GET /api/analytics/campaigns/{id}/performance
GET /api/analytics/brands/{slug}/summary
```

Retrieve analytics data.

**Response:**
```json
{
  "period": "2025-11-01 to 2025-11-14",
  "metrics": {
    "emails_sent": 1250,
    "open_rate": 0.34,
    "click_rate": 0.08,
    "conversions": 18
  }
}
```

## Configuration Schema

### Brand Configuration (`config/brands.yaml`)

```yaml
brands:
  buildly:
    name: "Buildly"
    slug: "buildly"
    tagline: "AI-powered product development"
    voice: "professional, technical"
    templates:
      email: "buildly_email"
      social: "buildly_social"
    primary_contact: "hello@buildly.io"
```

### Outreach Configuration (`config/outreach_config.yaml`)

```yaml
outreach:
  targets:
    - email
    - linkedin
    - twitter
  frequency: "daily"
  batch_size: 50
  retry_failed: true
  retry_attempts: 3
```

### Email Configuration (`config/email_config.yaml`)

```yaml
email:
  provider: "brevo"
  from_address: "marketing@buildly.io"
  from_name: "Buildly"
  reply_to: "support@buildly.io"
  templates_path: "templates/emails"
```

## Database Schema

### Campaigns Table

```sql
campaigns (
  id UUID PRIMARY KEY,
  brand_slug VARCHAR(50),
  name VARCHAR(255),
  status ENUM('draft', 'active', 'paused', 'completed'),
  content TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  scheduled_for TIMESTAMP
)
```

### Contacts Table

```sql
contacts (
  id UUID PRIMARY KEY,
  email VARCHAR(255),
  name VARCHAR(255),
  status ENUM('active', 'inactive', 'bounced'),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

### Email Events Table

```sql
email_events (
  id UUID PRIMARY KEY,
  campaign_id UUID,
  contact_id UUID,
  event_type ENUM('sent', 'opened', 'clicked', 'bounced'),
  timestamp TIMESTAMP,
  metadata JSON
)
```

## Environment Variables Reference

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `FLASK_ENV` | string | Yes | - | `development` or `production` |
| `OLLAMA_HOST` | string | Yes | - | Ollama service URL |
| `SECRET_KEY` | string | Yes | - | Flask secret key |
| `DATABASE_URL` | string | No | SQLite | Database connection string |
| `OPENAI_API_KEY` | string | No | - | OpenAI API key (if using OpenAI) |
| `GOOGLE_ADS_CLIENT_ID` | string | No | - | Google OAuth client ID |
| `GOOGLE_ADS_CLIENT_SECRET` | string | No | - | Google OAuth client secret |
| `BREVO_API_KEY` | string | No | - | Brevo email service API key |
| `LOG_LEVEL` | string | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_WORKERS` | integer | No | `4` | Background job worker threads |

## File Structure

```
/src/
  /api/               - Flask API endpoints
  /automation/        - Core automation engine
  /models/            - Data models
  /services/          - Business logic services
  /config/            - Configuration management
  /templates/         - Email & message templates
/tests/
  /smoke/             - Health & basic tests
  /crud/              - CRUD operation tests
/ops/
  /Dockerfile         - Container build
  /docker-compose.yml - Multi-service compose
  /helm/              - Kubernetes charts
/devdocs/             - Complete documentation
```

## Third-Party Integrations

### Ollama (AI Content Generation)
- **Service:** Local or remote LLM inference
- **Endpoint:** `OLLAMA_HOST` environment variable
- **Models:** mistral, llama2, neural-chat, etc.

### Brevo (Email Service)
- **API Key:** `BREVO_API_KEY`
- **Rate Limit:** 300 requests/minute
- **Webhook:** Delivery status callbacks

### Google Ads (Campaign Management)
- **OAuth Flow:** 3-legged auth via `config/google_oauth.yaml`
- **API Version:** v13+

### Mastodon (Social Publishing)
- **Base URL:** Configurable per brand
- **Token:** Stored in `config/mastodon_tokens.json`

## Error Codes

| Code | Meaning | Resolution |
|------|---------|-----------|
| 400 | Bad Request | Check request format and required fields |
| 401 | Unauthorized | Verify API credentials |
| 429 | Rate Limited | Wait before retrying |
| 500 | Server Error | Check logs, contact support |
| 503 | Service Unavailable | Check Ollama/database connectivity |

## Performance Targets

- Campaign creation: < 100ms
- Content generation: 5-30s (depends on model)
- Email send: < 2s per batch of 100
- Dashboard load: < 1s
- API response: < 200ms (p95)

## Testing

See **tests/** for smoke tests and CRUD checks. Run:

```bash
pytest tests/smoke/ -v
pytest tests/crud/ -v
```

---

For detailed examples and workflows, see **SETUP.md** and **OPERATIONS.md**.
