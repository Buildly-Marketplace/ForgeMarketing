# Database Configuration Guide

ForgeMarketing supports **SQLite** (local development), **PostgreSQL**, and **MySQL** for production deployments.

## Quick Start

### Local Development (SQLite - default)
No configuration needed. The app automatically uses SQLite at `data/marketing_dashboard.db`.

### Remote Database (PostgreSQL or MySQL)
Set the `DATABASE_URL` environment variable:

```bash
# PostgreSQL (Google Cloud SQL, Digital Ocean, Supabase, etc.)
export DATABASE_URL="postgresql://user:password@host:5432/forgemarketing"

# MySQL (Google Cloud SQL, Digital Ocean, PlanetScale, etc.)
export DATABASE_URL="mysql://user:password@host:3306/forgemarketing"
```

## Environment Variable

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Full database connection URL | `sqlite:///data/marketing_dashboard.db` |

The app reads `DATABASE_URL` at startup. If not set, it falls back to local SQLite.

## Driver Installation

The required drivers are in `requirements.txt`:

```bash
pip install -r requirements.txt
```

| Database | Python Driver | Package |
|----------|--------------|---------|
| SQLite | Built-in | (none needed) |
| PostgreSQL | psycopg2 | `psycopg2-binary>=2.9.0` |
| MySQL | mysqlclient | `mysqlclient>=2.2.0` |

## Deployment Examples

### Digital Ocean Managed Database (PostgreSQL)
1. Create a PostgreSQL database in Digital Ocean
2. Copy the connection string from the database dashboard
3. Set as environment variable:
```bash
export DATABASE_URL="postgresql://doadmin:PASSWORD@db-host-do-user-XXX.b.db.ondigitalocean.com:25060/forgemarketing?sslmode=require"
```

### Google Cloud SQL (PostgreSQL)
1. Create a Cloud SQL PostgreSQL instance
2. Create a database named `forgemarketing`
3. Set the connection URL:
```bash
export DATABASE_URL="postgresql://postgres:PASSWORD@/forgemarketing?host=/cloudsql/PROJECT:REGION:INSTANCE"
```

### Google Cloud SQL (MySQL)
```bash
export DATABASE_URL="mysql://root:PASSWORD@/forgemarketing?unix_socket=/cloudsql/PROJECT:REGION:INSTANCE"
```

## Architecture

### Main Application Database
- Used by Flask-SQLAlchemy for all ORM models (Brand, BrandEmailConfig, MarketingCalendar, etc.)
- Configured in `dashboard/app.py`
- Connection pooling enabled for remote databases (pool_size=10, pool_recycle=300s)

### Activity Tracker Database
- Used by `automation/activity_tracker.py` for analytics tracking
- Also reads `DATABASE_URL` — when set, activity tables live in the same remote database
- When `DATABASE_URL` is not set, uses a separate SQLite file at `data/activity_tracker.db`

## Notes

- The `postgres://` scheme (used by Heroku and some providers) is automatically converted to `postgresql://`
- SQLAlchemy's JSON column type works natively across all three backends
- Enum columns use VARCHAR with constraints (cross-DB compatible)
- `db.create_all()` runs at startup to ensure all tables exist
