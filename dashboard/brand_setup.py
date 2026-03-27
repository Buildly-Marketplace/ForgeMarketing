"""
Brand Auto-Setup Module
Scrapes a website URL to auto-discover brand information:
  - Meta description, title, Open Graph data
  - Logo/favicon URL
  - Social media links
  - Theme color
"""

import re
import requests
from urllib.parse import urljoin, urlparse
from typing import Dict, Any, Optional


def discover_brand(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Fetch a website and extract brand metadata.
    Returns a dict with discovered fields (all optional except url).
    """
    result: Dict[str, Any] = {
        'website_url': url,
        'description': '',
        'logo_url': '',
        'theme_color': '',
        'social_links': {},
        'meta_title': '',
    }

    parsed = urlparse(url)
    if not parsed.scheme:
        url = 'https://' + url
        result['website_url'] = url

    try:
        resp = requests.get(
            url,
            timeout=timeout,
            headers={'User-Agent': 'ForgeMarketing-Setup/1.0'},
            allow_redirects=True,
        )
        resp.raise_for_status()
    except requests.RequestException:
        return result

    html = resp.text
    final_url = resp.url
    result['website_url'] = final_url

    # --- Meta title ---
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        result['meta_title'] = _clean(m.group(1))

    # --- Meta description ---
    for pattern in [
        r'<meta\s+[^>]*property=["\']og:description["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+[^>]*content=["\'](.*?)["\']\s+property=["\']og:description["\']',
        r'<meta\s+[^>]*name=["\']description["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+[^>]*content=["\'](.*?)["\']\s+name=["\']description["\']',
    ]:
        m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if m and m.group(1).strip():
            result['description'] = _clean(m.group(1))
            break

    # --- OG image / logo ---
    for pattern in [
        r'<meta\s+[^>]*property=["\']og:image["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+[^>]*content=["\'](.*?)["\']\s+property=["\']og:image["\']',
    ]:
        m = re.search(pattern, html, re.IGNORECASE)
        if m and m.group(1).strip():
            result['logo_url'] = urljoin(final_url, m.group(1).strip())
            break

    # Fallback: apple-touch-icon or first favicon link
    if not result['logo_url']:
        for pattern in [
            r'<link\s+[^>]*rel=["\']apple-touch-icon["\']\s+[^>]*href=["\'](.*?)["\']',
            r'<link\s+[^>]*href=["\'](.*?)["\']\s+[^>]*rel=["\']apple-touch-icon["\']',
            r'<link\s+[^>]*rel=["\']icon["\']\s+[^>]*href=["\'](.*?)["\']',
            r'<link\s+[^>]*href=["\'](.*?)["\']\s+[^>]*rel=["\']icon["\']',
        ]:
            m = re.search(pattern, html, re.IGNORECASE)
            if m and m.group(1).strip():
                result['logo_url'] = urljoin(final_url, m.group(1).strip())
                break

    # --- Theme color ---
    for pattern in [
        r'<meta\s+[^>]*name=["\']theme-color["\']\s+content=["\'](.*?)["\']',
        r'<meta\s+[^>]*content=["\'](.*?)["\']\s+name=["\']theme-color["\']',
    ]:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            result['theme_color'] = m.group(1).strip()
            break

    # --- Social links ---
    social_patterns = {
        'twitter': r'https?://(?:www\.)?(twitter\.com|x\.com)/[A-Za-z0-9_]+',
        'linkedin': r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[A-Za-z0-9_-]+',
        'github': r'https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+',
        'facebook': r'https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.]+',
        'instagram': r'https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.]+',
        'youtube': r'https?://(?:www\.)?youtube\.com/(?:@|c/|channel/)[A-Za-z0-9_-]+',
        'mastodon': r'https?://[A-Za-z0-9.-]+/@[A-Za-z0-9_]+',
        'bluesky': r'https?://bsky\.app/profile/[A-Za-z0-9._-]+',
    }
    for platform, pattern in social_patterns.items():
        m = re.search(pattern, html)
        if m:
            result['social_links'][platform] = m.group(0)

    return result


def suggest_brand_name(display_name: str) -> str:
    """Generate a slug-style brand name from the display name."""
    slug = re.sub(r'[^a-z0-9]+', '', display_name.lower())
    return slug or 'mybrand'


def _clean(text: str) -> str:
    """Strip HTML entities and excess whitespace."""
    text = re.sub(r'&#?\w+;', ' ', text)
    text = re.sub(r'<[^>]+>', '', text)
    return ' '.join(text.split()).strip()
