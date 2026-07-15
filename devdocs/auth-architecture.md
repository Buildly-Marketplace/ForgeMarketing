# Auth Architecture: Gateway, ForgeMarketing, Producer

This documents how login/auth actually works across the three processes as of
2026-07-09, what was broken, and what was (and wasn't) fixed in this pass.

## The three processes

| Process | File | Port | Framework |
|---|---|---|---|
| Gateway (login + app launcher) | `gateway_app.py` | 5000 | Flask + Flask-Login |
| Marketing Hub | `dashboard/app.py` | 8002 | Flask |
| Producer (podcast tool) | `Producer/manage.py` | 8001 | Django |

All three sit behind one nginx (`deploy/nginx.conf`), path-routed at `/`,
`/marketing/`, `/producer/`.

## What "one login, two permission sets" was supposed to mean

- A user logs in **once**, at the gateway.
- Marketing Hub and Producer each keep their **own** role/permission model
  (ForgeMarketing: `User.is_admin` + per-brand `UserBrand.role`; Producer:
  `Role` enum with a hierarchy, assigned per-Show via `ShowRoleAssignment`,
  overridable per-Episode).
- Switching between the two apps shouldn't require logging in twice.

## What was actually implemented (before this pass)

**Only the gateway half of this existed.** The gateway has real Flask-Login
auth (`gateway_app.py`, `dashboard/auth.py`) against a shared `users` table.
On successful login it also mints a second artifact — a `forge_auth` cookie,
HMAC-signed with `SHARED_AUTH_SECRET` — clearly intended as a cross-app SSO
token for Producer to verify.

**That token is never read by anything.** Confirmed by exhaustive grep:
- No file named `gateway_auth.py` (or equivalent) exists anywhere in Producer.
- `forge_auth` / `SHARED_AUTH_SECRET` have zero references outside the one
  file that mints them (`dashboard/auth.py`).
- Producer's login (`/producer/auth/login/`) is 100% stock Django
  `contrib.auth`, against Producer's own local `auth_user` table. A gateway
  login buys you nothing there — hitting any `LoginRequiredMixin` view in
  Producer bounces you to Producer's own separate login form.
- **`dashboard/app.py` — the process actually serving Marketing Hub on port
  8002 — had no Flask-Login instance at all.** No `LoginManager`, no
  `user_loader`, nothing. It never read the `forge_auth` cookie or the
  Flask-Login session cookie either. It ran wide open by omission.

So prior to this pass: "one login" existed only for the gateway's own routes.
Marketing Hub was unauthenticated regardless of login state. Producer required
a second, fully independent login with fully independent credentials/roles.

## Bugs found (file:line)

1. **`dashboard/app.py` had zero auth enforcement.** No `LoginManager`
   attached to the Flask app object that's actually deployed on port 8002
   (`deploy/supervisord.conf` runs `dashboard.app:app` directly, not behind
   the gateway process). Every route was reachable unauthenticated.
2. **Fail-open admin guard**, `dashboard/admin_api.py:19-40` (pre-fix): both
   `admin_required` and the blueprint's `before_request` did
   `if not hasattr(current_app, 'login_manager'): return None` — i.e.
   *skip the check* when no LoginManager is present, which was always true
   on the actual deployed process. This made `/api/admin/*` (brand configs,
   API credentials, system config, audit logs) fully open in production,
   not just "missing a decorator."
3. **`marketing_calendar_api.py` and `lead_radar_api.py` had no auth check
   of any kind** — not even the broken conditional kind. All calendar/task
   CRUD and all lead/contact data was open to anyone who could reach port
   8002.
4. **Secret-key env var mismatch**, `gateway_app.py:26` vs old
   `dashboard/app.py:155`: gateway reads `FLASK_SECRET_KEY`, dashboard read
   a different var, `DASHBOARD_SECRET_KEY`. Since only `FLASK_SECRET_KEY` is
   set in `.env`, the two processes were signing/verifying sessions with
   different keys — a session cookie from one would never validate on the
   other, even before the missing-LoginManager issue.
5. **Duplicated import block**, old `dashboard/app.py:7-17` repeated almost
   verbatim at `34-44` (imports, `project_root`/`sys.path` setup) — dead
   code from a copy-paste, no functional bug but pure clutter.
6. **Insecure hardcoded fallback secrets, confirmed live in this env**:
   `dashboard/auth.py:22` `SHARED_AUTH_SECRET` defaults to the literal
   `'forge-shared-auth-2025'`; `dashboard/app.py` secret_key defaulted to
   `'marketing-automation-dashboard-2025'`. Neither `SHARED_AUTH_SECRET` nor
   `DASHBOARD_SECRET_KEY` are set in `.env`, so both insecure defaults were
   live. (Not fully fixed this pass — see "Not fixed" below.)
7. **Producer git submodule was broken.** `.gitmodules` pointed at
   `Buildly-Labs/Producer.git`, a different/stale fork from the one actually
   in local use (`Buildly-Marketplace/Producer`, matching the working
   checkout at `buildly/THEFORGE/Producer`). The submodule was also never
   properly `git submodule add`-ed to the index, so a fresh clone got an
   empty `Producer/` directory and `git submodule update --init` failed
   outright. Fixed: repointed `.gitmodules` at `Buildly-Marketplace/Producer`
   and re-added the submodule properly (commit `f82382c`).

## What was fixed in this pass (scope: close the open-API hole, not build full SSO)

Per explicit decision, this pass does **not** build the cross-app SSO
handshake (Producer still has its own independent login). It closes the
concrete security hole: Marketing Hub's APIs being wide open.

- `dashboard/app.py`: added a real `flask_login.LoginManager` (mirroring
  `gateway_app.py`'s setup) with a matching `user_loader`, and registered
  `auth_bp` so `/login`/`/logout` work when Marketing Hub is hit directly
  (not just via the gateway). Secret key now falls back through
  `DASHBOARD_SECRET_KEY` → `FLASK_SECRET_KEY` → the old hardcoded literal,
  so it agrees with the gateway when only `FLASK_SECRET_KEY` is set.
- `dashboard/admin_api.py`: removed the `hasattr(current_app, 'login_manager')`
  conditional bypass entirely — the guard now unconditionally requires
  `current_user.is_authenticated`.
- `dashboard/marketing_calendar_api.py`: added a `before_request` guard
  requiring authentication (JSON 401 on failure — this blueprint is API-only).
- `dashboard/lead_radar_api.py`: added a `before_request` guard that returns
  JSON 401 for `/api/*` routes and redirects HTML page routes
  (`/lead-radar`, `/leads`, etc.) to `/login?next=<path>`.
- `dashboard/auth.py`: `login()` now honors a `next` query/form param to
  redirect back to the originally-requested page after login, restricted to
  same-site relative paths only (`_safe_next_url`) to prevent open-redirect
  abuse.
- `dashboard/templates/login.html`: carries `next` through the POST via a
  hidden field.
- Removed the duplicated import block in `dashboard/app.py`.

Verified with a Flask test client: unauthenticated requests to
`/api/admin/brands`, `/api/marketing/campaigns`, and `/api/leads` now return
401; `/lead-radar` redirects to `/login?next=/lead-radar`; a malicious
`next` value (`https://evil.example.com/...`) is sanitized to `/`.

## Not fixed in this pass (deferred, flagged for follow-up)

- **No real cross-app SSO.** Producer still has a fully separate login and
  user table. A user must log in twice. The `forge_auth` cookie is still
  minted but still unread by anyone — it's dead code until Producer gets a
  verifier. Building this properly requires: a verifier in Producer, an
  explicit user-identity link (there's no shared UUID/email mapping table
  today — a person is two unrelated accounts, not one identity with two role
  sets), and a decision on how ForgeMarketing's binary `is_admin` maps onto
  Producer's five-level `Role` hierarchy. Recommend a dedicated follow-up
  pass for this.
- **Hardcoded insecure default secrets remain** (`SHARED_AUTH_SECRET`,
  `DASHBOARD_SECRET_KEY`/`FLASK_SECRET_KEY` literal fallback,
  Producer's `SECRET_KEY` fallbacks in `logic_service/settings/*.py`,
  Producer's `SHARED_AUTH_SECRET` fallback that doesn't even correspond to
  real verification code, default admin `changeme123`/`changeme`
  credentials). These should fail loudly at startup in production rather
  than silently falling back to a committed constant — deferred as a
  separate hardening pass since it touches deploy config, not just app code.
- **Logout doesn't propagate across apps** — moot today since there's no
  real SSO session to propagate, but will need addressing once SSO is built
  (single logout / back-channel logout).
- **DB config env-var mismatch** between gateway/dashboard
  (`DATABASE_ENGINE=mysql+mysqldb`-style SQLAlchemy dialect strings) and
  Producer (`DATABASE_ENGINE=postgresql`-style Django engine suffixes) — as
  shipped, `docker-compose.yml` doesn't actually set these for either
  service, so both fall back to independent local SQLite files regardless.
