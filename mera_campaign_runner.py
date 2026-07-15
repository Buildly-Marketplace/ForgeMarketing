#!/usr/bin/env python3
"""
My Evil Robot Army — Music Promo Email Campaign Runner
Uses ForgeMarketing's UnifiedEmailService to send personalized outreach emails.

Usage:
    python3 mera_campaign_runner.py --preview          # Preview only (no sends)
    python3 mera_campaign_runner.py --send             # Send all emails
    python3 mera_campaign_runner.py --send --limit 3   # Send to first 3 contacts
    python3 mera_campaign_runner.py --send --type radio   # Only radio stations
    python3 mera_campaign_runner.py --send --type playlist # Only playlist curators

Run from: /Users/greglind/Projects/NullRecords/ForgeMarketing/
"""

import sys
import os
import csv
import time
import argparse
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

_log_handlers = [logging.StreamHandler()]
_log_file = PROJECT_ROOT / "logs" / "mera_campaign.log"
try:
    _log_handlers.append(logging.FileHandler(_log_file))
except PermissionError:
    pass  # log to console only if file write is restricted

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=_log_handlers,
)
log = logging.getLogger("MERA")

# ── Album Data ──────────────────────────────────────────────────────────────

ALBUMS = {
    "Oscillating Overthruster": {
        "year": "2026",
        "genre": "Nu Jazz / Experimental Electronic",
        "spotify": "https://open.spotify.com/artist/4PBJ1WON6gmxC1L35HHh69",
        "smart_link": "https://streamondistro.lnk.to/OscillatingOverthruster",
        "store": "https://www.nullrecords.com/store/",
        "apple": "https://music.apple.com/us/artist/my-evil-robot-army/1576251082",
        "description": "experimental electronic and nu jazz fused into something entirely new",
    },
    "Spiraling": {
        "year": "2025",
        "genre": "Nu Jazz / Ambient Electronic",
        "spotify": "https://open.spotify.com/artist/4PBJ1WON6gmxC1L35HHh69",
        "smart_link": "",
        "store": "https://www.nullrecords.com/store/",
        "apple": "https://music.apple.com/us/artist/my-evil-robot-army/1576251082",
        "description": "ambient, spiraling nu jazz with deep electronic textures",
    },
    "Space Jazz": {
        "year": "2024",
        "genre": "Nu Jazz / Lofi Jazz",
        "spotify": "https://open.spotify.com/artist/4PBJ1WON6gmxC1L35HHh69",
        "smart_link": "",
        "store": "https://www.nullrecords.com/store/",
        "apple": "https://music.apple.com/us/artist/my-evil-robot-army/1576251082",
        "description": "classic jazz structure taken into spacious, atmospheric lofi territory",
    },
}

# ── Email Templates ─────────────────────────────────────────────────────────

def build_email(contact: dict, album_name: str, template_type: str) -> tuple[str, str]:
    """Return (subject, body) for a contact + album combination."""
    alb = ALBUMS.get(album_name, ALBUMS["Oscillating Overthruster"])
    name = contact.get("name", "Music Director")
    station = contact.get("station_or_playlist", "your station/playlist")

    # Pick the best streaming link
    streaming_link = alb["smart_link"] if alb["smart_link"] else alb["spotify"]

    if template_type == "radio_new":
        subject = f"Music Submission — My Evil Robot Army | {album_name} ({alb['genre']})"
        body = f"""Hi {name},

My name is Greg Lind — I'm writing on behalf of My Evil Robot Army, an independent nu jazz and experimental electronic project on NullRecords.

Our latest album, {album_name} ({alb['year']}), is {alb['description']}. I think it would be a genuine fit for {station}.

Stream / Smart Link: {streaming_link}
Spotify (Artist Page): {alb['spotify']}
Apple Music: {alb['apple']}
Lossless Store: {alb['store']}

Happy to send a WAV/FLAC broadcast-quality file via WeTransfer or Dropbox on request.

Thanks for your time and for the work you do supporting jazz.

Greg Lind | NullRecords
team@nullrecords.com
https://www.nullrecords.com"""

    elif template_type == "radio_spiraling":
        subject = f"Music Submission — My Evil Robot Army | Spiraling ({alb['genre']})"
        body = f"""Hi {name},

I'm reaching out on behalf of My Evil Robot Army on NullRecords. Our 2025 album Spiraling is {alb['description']} — I think it would resonate with your {station} audience.

Spotify (Artist Page): {alb['spotify']}
Apple Music: {alb['apple']}
Lossless Store: {alb['store']}

Happy to send broadcast-quality files on request.

Thanks,
Greg Lind | NullRecords
team@nullrecords.com
https://www.nullrecords.com"""

    elif template_type == "radio_space_jazz":
        subject = f"Music Submission — My Evil Robot Army | Space Jazz (Lofi Jazz / Nu Jazz)"
        body = f"""Hi {name},

I'm writing on behalf of My Evil Robot Army, an independent lofi jazz and nu jazz project on NullRecords.

Our 2024 album Space Jazz is {alb['description']}. I believe it would suit {station}'s programming well.

Spotify (Artist Page): {alb['spotify']}
Apple Music: {alb['apple']}
Lossless Store: {alb['store']}

Happy to provide broadcast-quality files on request.

Thanks for your time,
Greg Lind | NullRecords
team@nullrecords.com
https://www.nullrecords.com"""

    elif template_type == "playlist_lofi":
        subject = f"Playlist Submission — My Evil Robot Army | {album_name}"
        body = f"""Hey {name},

I produce under the name My Evil Robot Army on NullRecords — lofi jazz and nu jazz with an experimental electronic edge. I think {album_name} could sit well in {station}.

Spotify: {alb['spotify']}
{('Smart Link: ' + alb['smart_link']) if alb['smart_link'] else ''}

No pressure at all — appreciate you taking a listen if you get the chance.

Greg | NullRecords
https://www.nullrecords.com | team@nullrecords.com"""

    else:
        # Fallback generic
        subject = f"Music Submission — My Evil Robot Army | {album_name}"
        body = f"""Hi {name},

I'm reaching out on behalf of My Evil Robot Army, a nu jazz and experimental electronic project on NullRecords.

Stream {album_name}: {streaming_link}
Spotify (Artist Page): {alb['spotify']}
Store (lossless): {alb['store']}

Thanks,
Greg Lind | NullRecords | team@nullrecords.com"""

    return subject.strip(), body.strip()


# ── Brand / DB Setup ─────────────────────────────────────────────────────────

def ensure_nullrecords_brand() -> int:
    """Create NullRecords brand if it doesn't exist. Returns brand_id."""
    db_path = PROJECT_ROOT / "data" / "marketing_dashboard.db"
    if not db_path.exists():
        log.error(f"DB not found: {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    now = datetime.now().isoformat()

    try:
        existing = conn.execute('SELECT id FROM brands WHERE name="nullrecords"').fetchone()
        if existing:
            brand_id = existing["id"]
            log.info(f"NullRecords brand exists (id={brand_id})")
        else:
            conn.execute(
                "INSERT INTO brands (name, display_name, description, website_url, is_active, is_template, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)",
                ("nullrecords", "NullRecords / My Evil Robot Army",
                 "Independent music label — nu jazz, lofi, experimental electronic",
                 "https://www.nullrecords.com", 1, 0, now, now),
            )
            brand_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            log.info(f"Created NullRecords brand (id={brand_id})")

        # Copy email config from brand 1 if needed
        existing_cfg = conn.execute(
            "SELECT id FROM brand_email_configs WHERE brand_id=?", (brand_id,)
        ).fetchone()
        if not existing_cfg:
            src = conn.execute(
                "SELECT * FROM brand_email_configs WHERE brand_id=1"
            ).fetchone()
            if src:
                s = dict(src)
                conn.execute(
                    """INSERT INTO brand_email_configs
                       (brand_id,provider,api_key,api_token,smtp_host,smtp_port,
                        smtp_user,smtp_password,from_email,from_name,reply_to_email,
                        reply_to_name,is_primary,max_send_per_day,rate_limit_per_minute,
                        is_verified,created_at,updated_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (brand_id, s["provider"], s["api_key"] or "", s["api_token"],
                     s["smtp_host"], s["smtp_port"], s["smtp_user"], s["smtp_password"],
                     "team@nullrecords.com", "NullRecords Music",
                     "team@nullrecords.com", "Greg Lind | NullRecords",
                     1, s["max_send_per_day"] or 50,
                     s["rate_limit_per_minute"] or 10, 1, now, now),
                )
                log.info(f"Created email config: team@nullrecords.com via {s['provider']}")
            else:
                log.warning("No source email config found on brand 1 — configure email in ForgeMarketing settings")

        conn.commit()
        return brand_id
    finally:
        conn.close()


# ── Main Campaign Logic ──────────────────────────────────────────────────────

def load_contacts(csv_path: str, contact_type: str = None) -> list[dict]:
    contacts = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if contact_type and row.get("type") != contact_type:
                continue
            contacts.append(row)
    return contacts


def run_campaign(args):
    preview = not args.send
    contact_type = args.type
    limit = args.limit
    csv_path = args.csv

    log.info("=" * 60)
    log.info("My Evil Robot Army — Music Promo Campaign")
    log.info(f"Mode: {'PREVIEW' if preview else 'LIVE SEND'}")
    log.info(f"Filter: {contact_type or 'all'}")
    log.info("=" * 60)

    # Ensure NullRecords brand exists in DB
    brand_id = ensure_nullrecords_brand()

    # Load contacts
    contacts = load_contacts(csv_path, contact_type)
    if limit:
        contacts = contacts[:limit]

    log.info(f"Loaded {len(contacts)} contacts")

    if not contacts:
        log.warning("No contacts found — check CSV path and filters")
        return

    if preview:
        log.info("\n--- EMAIL PREVIEWS ---\n")
        for i, c in enumerate(contacts, 1):
            subject, body = build_email(c, c.get("album_target", "Oscillating Overthruster"), c.get("template", "radio_new"))
            log.info(f"[{i}/{len(contacts)}] TO: {c['email']} ({c['station_or_playlist']})")
            log.info(f"  SUBJECT: {subject}")
            log.info(f"  BODY PREVIEW: {body[:200]}...")
            log.info("")
        log.info("Preview complete. Run with --send to send emails.")
        return

    # Live send via UnifiedEmailService
    try:
        from unified_email_service import UnifiedEmailService
        email_svc = UnifiedEmailService()
    except ImportError as e:
        log.error(f"Could not import UnifiedEmailService: {e}")
        log.error("Make sure you're running from the ForgeMarketing project root")
        sys.exit(1)

    sent = 0
    failed = 0
    skipped = 0

    for i, contact in enumerate(contacts, 1):
        email = contact.get("email", "").strip()
        if not email or "@" not in email:
            log.warning(f"[{i}] Skipping invalid email: {email}")
            skipped += 1
            continue

        album_name = contact.get("album_target", "Oscillating Overthruster")
        template_type = contact.get("template", "radio_new")

        subject, body = build_email(contact, album_name, template_type)

        log.info(f"[{i}/{len(contacts)}] Sending to {email} ({contact.get('station_or_playlist', '')})...")
        log.info(f"  Subject: {subject}")

        try:
            result = email_svc.send_email(
                brand="nullrecords",
                to_email=email,
                subject=subject,
                body=body,
                is_html=False,
                bcc_email="team@nullrecords.com",
            )

            if result.get("success") or result.get("status") in ("sent", "queued"):
                log.info(f"  ✅ Sent | service={result.get('service', 'unknown')}")
                sent += 1
            else:
                log.warning(f"  ⚠️  Uncertain result: {result}")
                sent += 1  # count as sent if no explicit error

        except Exception as exc:
            log.error(f"  ❌ Failed: {exc}")
            failed += 1

        # Rate limiting — be polite
        if i < len(contacts):
            time.sleep(2)

    log.info("\n" + "=" * 60)
    log.info(f"Campaign complete: {sent} sent, {failed} failed, {skipped} skipped")
    log.info("=" * 60)


# ── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="My Evil Robot Army promo email campaign runner"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--preview", action="store_true", default=True, help="Preview emails (default)")
    group.add_argument("--send", action="store_true", help="Actually send emails")

    parser.add_argument(
        "--type",
        choices=["radio", "playlist"],
        default=None,
        help="Filter by contact type",
    )
    parser.add_argument("--limit", type=int, default=None, help="Max emails to process")
    parser.add_argument(
        "--csv",
        default=str(PROJECT_ROOT / "mera_promo_contacts.csv"),
        help="Path to contacts CSV",
    )

    args = parser.parse_args()

    # If --send is explicitly passed, override the default preview=True
    if "--send" in sys.argv:
        args.preview = False

    run_campaign(args)
