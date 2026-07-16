#!/usr/bin/env python3
"""Content generation must be DB-brand-driven.

A brand created via the admin UI / onboarding (DB only, no filesystem
brand_config.yaml) must still resolve a usable content config, and unknown
brands must fail cleanly. Also verifies the outreach runner never falls back
to another brand's email copy.
"""
import os
import sys
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Use an isolated throwaway DB.
os.environ["DATABASE_URL"] = "sqlite:////tmp/test_brand_content_config.db"
pathlib.Path("/tmp/test_brand_content_config.db").unlink(missing_ok=True)

from dashboard.app import app  # noqa: E402
from dashboard.models import db, Brand, BrandSettings  # noqa: E402
from dashboard.lead_radar_models import OutreachTemplate  # noqa: E402


def _seed_brand():
    with app.app_context():
        db.create_all()
        if not Brand.query.filter_by(name="acme-widgets").first():
            b = Brand(name="acme-widgets", display_name="Acme Widgets",
                      description="We make the best widgets.", is_active=True)
            db.session.add(b)
            db.session.flush()
            s = BrandSettings(brand_id=b.id)
            s.set_advanced_settings({"marketing_profile": {
                "product_type": "B2B widget automation platform",
                "target_audience": "operations managers, procurement leads",
                "brand_voice_notes": "confident, friendly, no jargon",
                "primary_cta": "Start a free trial",
                "default_hashtags": "#widgets, #automation, #b2b",
                "visual_style_notes": "clean, modern",
            }})
            db.session.add(s)
            db.session.commit()


def test_content_config_resolves_from_db_for_admin_created_brand():
    _seed_brand()
    from automation.ai.ollama_integration import AIContentGenerator
    gen = AIContentGenerator()
    cfg = gen.resolve_brand_config("acme-widgets")

    assert cfg["brand"]["name"] == "Acme Widgets"
    assert cfg["brand"]["description"] == "We make the best widgets."
    assert cfg["voice"]["tone"] == ["confident", "friendly", "no jargon"]
    assert cfg["key_messages"]["primary"] == "B2B widget automation platform"
    assert cfg["target_audience"]["primary"] == ["operations managers", "procurement leads"]
    assert cfg["social_media"]["hashtags"] == ["widgets", "automation", "b2b"]
    # top-level alias used by one fallback branch in the email generator
    assert cfg["name"] == "Acme Widgets"


def test_unknown_brand_raises():
    from automation.ai.ollama_integration import AIContentGenerator
    gen = AIContentGenerator()
    try:
        gen.resolve_brand_config("no-such-brand")
        assert False, "expected ValueError for unknown brand"
    except ValueError:
        pass


def test_outreach_never_uses_another_brands_template():
    _seed_brand()
    with app.app_context():
        if not OutreachTemplate.query.filter_by(brand_name="acme-widgets").first():
            db.session.add(OutreachTemplate(
                brand_name="acme-widgets", template_name="default", channel="email",
                subject_template="Hello from Acme",
                body_template="Hi {contact_name}, {personalization} — Acme Widgets",
                is_active=True,
            ))
            db.session.commit()

    from automation.run_brand_outreach import BrandOutreachRunner

    # Brand with its own DB template -> gets it.
    t = BrandOutreachRunner("acme-widgets")._load_email_template()
    assert t and "Acme" in t["subject"]

    # Brand with no template + no builtin -> None (must NOT return buildly's copy).
    assert BrandOutreachRunner("brand-with-nothing")._load_email_template() is None
