# Setup Guide

Get ForgeMark running on your system in minutes.

## Prerequisites

- **Python 3.8+** (check with `python --version`)
- **Ollama** (for local AI content generation): https://ollama.ai
- **Git**
- **Docker** (optional, for containerized deployment)

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/buildlyio/marketing.git
cd marketing
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

**Required environment variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `OLLAMA_HOST` | Ollama server address | `localhost:11434` |
| `FLASK_ENV` | Flask environment | `development` or `production` |
| `DATABASE_URL` | Database connection (optional) | `sqlite:///marketing.db` |
| `OPENAI_API_KEY` | OpenAI key (if using OpenAI instead of Ollama) | `sk-...` |
| `GOOGLE_ADS_CLIENT_ID` | Google Ads OAuth client | `*.apps.googleusercontent.com` |
| `GOOGLE_ADS_CLIENT_SECRET` | Google Ads OAuth secret | `GOCSPX-...` |
| `BREVO_API_KEY` | Brevo/Sendinblue email API | `xkeysib-...` |

### 3. Start Ollama

```bash
ollama serve
```

In a new terminal, pull a model:

```bash
ollama pull mistral
```

### 4. Run the Application

```bash
python -m automation.run_unified_outreach
```

Or start the Flask dashboard:

```bash
python -m flask run
```

The dashboard will be available at `http://localhost:5000`

## Configuration Files

- **`config/brands.yaml`** - Brand definitions and messaging templates
- **`config/outreach_config.yaml`** - Outreach campaign settings
- **`config/email_config.yaml`** - Email service configuration
- **`.env`** - Runtime environment variables

## Database Initialization

On first run, the system auto-creates SQLite databases:

- `outreach_automation.db` - Campaign and contact data
- `email_stats.db` - Email delivery tracking
- `cron_management.db` - Scheduled task state

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_HOST` environment variable
- Verify firewall doesn't block port 11434

### Missing API Keys
- Copy `.env.example` to `.env`
- Fill in required API keys for your providers
- App will fail loudly with helpful error messages

### Database Lock Error
- Ensure only one instance is running at a time
- Check for orphaned database locks: `rm *.db-lock` if present

## Next Steps

- See **OPERATIONS.md** for deployment instructions
- See **REFERENCE.md** for API and configuration details
- See **RELEASE_NOTES.md** for what's new in this version
