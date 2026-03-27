# ForgeMark Setup Guide

**One-command setup and deployment for ForgeMark marketing automation.**

## ⚡ Quick Start (30 Seconds)

```bash
# Navigate to project
cd marketing

# Run setup
./ops/startup.sh setup

# Start server
./ops/startup.sh start

# Access server at http://localhost:8002
```

That's it! The script handles everything automatically.

## 🛠️ Setup Script Features

The `ops/startup.sh` script:

1. **Verifies Prerequisites**
   - Checks Python 3.8+ is installed
   - Verifies Git (optional)

2. **Sets Up Environment**
   - Creates `.venv` if needed
   - Installs all dependencies from `requirements.txt`
   - Configures environment variables

3. **Validates Configuration**
   - Creates `.env` from `.env.example` if missing
   - Checks Ollama connectivity (non-blocking)
   - Verifies Flask app location

4. **Runs Smoke Tests**
   - Validates system is ready
   - Checks all required files exist

5. **Starts Server**
   - Runs on port 8002 by default
   - Uses Gunicorn if available, Flask dev server otherwise

## 📋 Usage Options

### Initial Setup
```bash
./ops/startup.sh setup
```

### Start Server (Port 8002)
```bash
./ops/startup.sh start
```

### Custom Port
```bash
./ops/startup.sh start --port 9000
```

### Fresh Installation
```bash
./ops/startup.sh setup --clean
```

Removes existing `.venv` and reinstalls everything from scratch.

### Skip Virtual Environment
```bash
./ops/startup.sh setup --no-venv
```

Uses existing virtual environment without recreating it.

### Stop Server
```bash
./ops/startup.sh stop
```

### Restart Server
```bash
./ops/startup.sh restart
```

### Show Help
```bash
./ops/startup.sh --help
```

## 🔧 Configuration

### Environment Variables

The script looks for these variables:

- **FLASK_ENV** - `development` or `production` (default: development)
- **OLLAMA_HOST** - Ollama server (default: localhost:11434)
- **DATABASE_URL** - Database connection (optional)

### .env File

The script creates `.env` from `.env.example` if it doesn't exist. Edit it with:

```bash
cp .env.example .env
# Then edit .env with your values
```

**Key variables to set:**
- `FLASK_ENV` - Set to `production` for deployment
- `OLLAMA_HOST` - Point to your Ollama server
- `BREVO_API_KEY` - Email service API key
- `GOOGLE_ADS_*` - Google Ads credentials

## 🧪 Smoke Tests

Before starting, verify everything is ready:

```bash
python tests/smoke_check.py
```

Checks:
- Environment variables are set
- Required files exist
- Configuration is valid
- Deployment files are present

## 🐛 Troubleshooting

### Port Already in Use
```bash
./ops/startup.sh start --port 9000
```

### Python Not Found
Install Python 3.8+: https://python.org

### Ollama Not Responding
```bash
# In another terminal
ollama serve

# Optional: Download a model
ollama pull mistral
```

### Virtual Environment Issues
```bash
./ops/startup.sh setup --clean
```

### Missing Dependencies
Make sure `requirements.txt` exists in project root.

## 📚 What Happens During Setup

```
ForgeMark Setup and Deployment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Checking Prerequisites
   ✓ Python 3.10.0 found
   ✓ Git is installed

2. Setting Up Virtual Environment
   ✓ Virtual environment activated

3. Installing Dependencies
   ✓ Python package tools upgraded
   ✓ All dependencies installed

4. Checking Configuration
   ✓ .env file exists
   ℹ FLASK_ENV: development
   ℹ OLLAMA_HOST: localhost:11434
   ℹ Server port: 8002

5. Checking Optional Services
   ✓ Ollama service is available at localhost:11434

6. Running Smoke Tests
   ✓ Smoke tests passed

7. Starting ForgeMark Server
   ═════════════════════════════════════
   ForgeMark Server Starting
   Port: 8002
   URL: http://localhost:8002
   Press Ctrl+C to stop
   ═════════════════════════════════════
```

## 🚀 Next Steps

1. **Open dashboard** - Navigate to http://localhost:8002
2. **Configure brands** - Update brand settings in `config/brands.yaml`
3. **Set up integrations** - Configure API keys for your services
4. **Run tests** - Execute tests to verify integrations
5. **Deploy** - See `ops/README.md` for Docker/Kubernetes deployment

## 📦 Deployment Options

### Local Development
```bash
./ops/startup.sh setup
./ops/startup.sh start
```

### Docker
```bash
docker-compose -f ops/docker-compose.yml up -d
```

### Kubernetes
```bash
helm install forgemark ops/helm/forgemark/ -n forgemark --create-namespace
```

## 📖 Additional Documentation

- **Quick Start** - See `README.md`
- **Installation & Config** - See `devdocs/SETUP.md`
- **Deployment** - See `devdocs/OPERATIONS.md` and `ops/README.md`
- **API Reference** - See `devdocs/REFERENCE.md`
- **Tests & Utilities** - See `tests/README.md`

## 💡 Common Commands

```bash
# Initial setup
./ops/startup.sh setup

# Start server with default port
./ops/startup.sh start

# Start with custom port
./ops/startup.sh start --port 9000

# Clean installation
./ops/startup.sh setup --clean

# Stop server
./ops/startup.sh stop

# Restart server
./ops/startup.sh restart

# Run smoke tests
python tests/smoke_check.py

# View logs
tail -f ops/server.log

# Run integration tests
python tests/test_google_ads_connection.py
```

## 🆘 Need Help?

1. Check `SUPPORT.md` for support options
2. Review `devdocs/SETUP.md` for detailed setup
3. Run smoke tests: `python tests/smoke_check.py`
4. Check logs in `logs/` directory
5. Review test results: `tests/README.md`

---

**Ready to get started?** Run `./ops/startup.sh setup && ./ops/startup.sh start` now! 🚀
