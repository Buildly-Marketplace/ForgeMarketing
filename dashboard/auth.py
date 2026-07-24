"""
Authentication blueprint — login, logout, brand switching.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import hashlib
import hmac
import json
import logging
import os
import time

from dashboard.models import db, User, UserBrand, Brand, SystemConfig

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)


def _safe_next_url(candidate: str) -> str:
    """Only allow same-site, relative redirect targets to prevent open redirects."""
    if candidate and candidate.startswith('/') and not candidate.startswith('//'):
        return candidate
    return url_for('index')


def _configured_admin_email() -> str:
    config = SystemConfig.query.filter_by(key='admin_email').first()
    return (config.value or '').strip().lower() if config else ''


def _initial_account_setup_available() -> bool:
    """Permit one local bootstrap only for the email supplied in onboarding."""
    admin_email = _configured_admin_email()
    return bool(admin_email and User.query.filter_by(email=admin_email).first() is None)

# Shared secret for cross-app auth cookie (must match Django setting)
_AUTH_COOKIE_SECRET = os.getenv('SHARED_AUTH_SECRET', 'forge-shared-auth-2025')
AUTH_COOKIE_NAME = 'forge_auth'
AUTH_COOKIE_MAX_AGE = 60 * 60 * 24 * 14  # 14 days


def _sign_auth_cookie(email: str, display_name: str) -> str:
    """Create a signed auth token: base64(json) + '.' + hmac signature."""
    payload = json.dumps({
        'email': email,
        'name': display_name,
        'ts': int(time.time()),
    }, separators=(',', ':'))
    sig = hmac.new(_AUTH_COOKIE_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    import base64
    return base64.urlsafe_b64encode(payload.encode()).decode() + '.' + sig


# ── HTML routes ──────────────────────────────────────────────

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    next_url = _safe_next_url(request.args.get('next') or request.form.get('next') or '')

    if current_user.is_authenticated:
        return redirect(next_url)

    if request.method == 'GET' and _initial_account_setup_available():
        # Avoid showing an unusable login form when onboarding has recorded an
        # owner email but that owner has never created their first password.
        return redirect(url_for('auth.setup_account', next=next_url))

    if request.method == 'GET':
        return render_template(
            'login.html', next=next_url,
            setup_available=_initial_account_setup_available(),
            setup_url=url_for('auth.setup_account', next=next_url),
        )

    # POST — either JSON or form
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''

    if not email or not password:
        msg = 'Email and password are required.'
        if request.is_json:
            return jsonify({'success': False, 'error': msg}), 400
        flash(msg, 'error')
        return render_template('login.html'), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        msg = 'Invalid email or password.'
        if request.is_json:
            return jsonify({'success': False, 'error': msg}), 401
        flash(msg, 'error')
        return render_template('login.html'), 401

    if not user.is_active:
        msg = 'Account is disabled.'
        if request.is_json:
            return jsonify({'success': False, 'error': msg}), 403
        flash(msg, 'error')
        return render_template('login.html'), 403

    login_user(user)
    user.last_login_at = datetime.utcnow()
    db.session.commit()

    # Set default active brand
    brands = user.get_brands()
    if brands:
        session['active_brand_id'] = brands[0].id
    elif user.is_admin:
        first = Brand.query.filter_by(is_active=True).first()
        if first:
            session['active_brand_id'] = first.id

    # Build the auth cookie for cross-app SSO
    auth_token = _sign_auth_cookie(user.email, user.display_name or user.email)

    if request.is_json:
        resp = make_response(jsonify({'success': True, 'redirect': next_url}))
    else:
        resp = make_response(redirect(next_url))

    resp.set_cookie(
        AUTH_COOKIE_NAME, auth_token,
        max_age=AUTH_COOKIE_MAX_AGE,
        path='/',
        httponly=True,
        samesite='Lax',
        secure=request.is_secure,
    )
    return resp


@auth_bp.route('/setup-account', methods=['GET', 'POST'])
def setup_account():
    """Create the one initial local admin account after brand onboarding.

    Onboarding records the owner's email but deliberately does not collect a
    password. This route turns that recorded owner into a real login exactly
    once, then signs them in and assigns ownership of active brands.
    """
    next_url = _safe_next_url(request.args.get('next') or request.form.get('next') or '')
    if current_user.is_authenticated:
        return redirect(next_url)

    admin_email = _configured_admin_email()
    if not admin_email or not _initial_account_setup_available():
        flash('An initial account is already set up. Sign in with that account, or ask an administrator to create one.', 'error')
        return redirect(url_for('auth.login', next=next_url))

    if request.method == 'GET':
        return render_template('setup_account.html', admin_email=admin_email, next=next_url)

    password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm_password') or ''
    if len(password) < 8:
        flash('Choose a password with at least 8 characters.', 'error')
        return render_template('setup_account.html', admin_email=admin_email, next=next_url), 400
    if password != confirm_password:
        flash('The passwords do not match.', 'error')
        return render_template('setup_account.html', admin_email=admin_email, next=next_url), 400

    user = User(email=admin_email, display_name=admin_email.split('@')[0], is_admin=True, must_change_password=False)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    active_brands = Brand.query.filter_by(is_active=True).all()
    for brand in active_brands:
        db.session.add(UserBrand(user_id=user.id, brand_id=brand.id, role='owner'))
    db.session.commit()

    login_user(user)
    user.last_login_at = datetime.utcnow()
    if active_brands:
        session['active_brand_id'] = active_brands[0].id
        session['active_brand_name'] = active_brands[0].name
    db.session.commit()

    auth_token = _sign_auth_cookie(user.email, user.display_name or user.email)
    resp = make_response(redirect(next_url))
    resp.set_cookie(AUTH_COOKIE_NAME, auth_token, max_age=AUTH_COOKIE_MAX_AGE,
                    path='/', httponly=True, samesite='Lax', secure=request.is_secure)
    return resp


@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('active_brand_id', None)
    logout_user()
    resp = make_response(redirect(url_for('auth.login')))
    resp.delete_cookie(AUTH_COOKIE_NAME, path='/')
    return resp


# ── Force password change ────────────────────────────────────

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')

    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    new_password = (data.get('new_password') or '').strip()
    confirm_password = (data.get('confirm_password') or '').strip()

    if not new_password or len(new_password) < 8:
        msg = 'Password must be at least 8 characters.'
        if request.is_json:
            return jsonify({'success': False, 'error': msg}), 400
        flash(msg, 'error')
        return render_template('change_password.html'), 400

    if new_password != confirm_password:
        msg = 'Passwords do not match.'
        if request.is_json:
            return jsonify({'success': False, 'error': msg}), 400
        flash(msg, 'error')
        return render_template('change_password.html'), 400

    current_user.set_password(new_password)
    current_user.must_change_password = False
    db.session.commit()

    if request.is_json:
        return jsonify({'success': True, 'redirect': url_for('index')})
    flash('Password updated successfully.', 'success')
    return redirect(url_for('index'))


# ── Brand switching ──────────────────────────────────────────

@auth_bp.route('/switch-brand/<int:brand_id>', methods=['POST'])
@login_required
def switch_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if not brand or not brand.is_active:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Brand not found'}), 404
        flash('Brand not found', 'error')
        return redirect('/')

    if not current_user.has_brand_access(brand_id):
        if request.is_json:
            return jsonify({'success': False, 'error': 'Access denied'}), 403
        flash('You do not have access to that brand', 'error')
        return redirect('/')

    session['active_brand_id'] = brand_id
    session['active_brand_name'] = brand.name

    if request.is_json:
        return jsonify({'success': True, 'brand': brand.to_dict()})

    return redirect(request.referrer or '/')


# ── User management API (admin only) ────────────────────────

@auth_bp.route('/api/users', methods=['GET'])
@login_required
def list_users():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin required'}), 403

    users = User.query.all()
    return jsonify({'success': True, 'users': [u.to_dict() for u in users]})


@auth_bp.route('/api/users', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin required'}), 403

    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    display_name = data.get('display_name', '')
    brand_ids = data.get('brand_ids', [])

    if not email or not password:
        return jsonify({'success': False, 'error': 'email and password required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'error': 'Email already exists'}), 409

    user = User(email=email, display_name=display_name)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    for bid in brand_ids:
        brand = Brand.query.get(bid)
        if brand:
            db.session.add(UserBrand(user_id=user.id, brand_id=brand.id, role='editor'))

    db.session.commit()
    return jsonify({'success': True, 'user': user.to_dict()}), 201
