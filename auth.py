"""
Authentication utilities
"""
from fasthtml.common import RedirectResponse
from config import VALID_CREDENTIALS


def validate_credentials(email: str, password: str) -> bool:
    """Validate user credentials"""
    return VALID_CREDENTIALS.get(email) == password


def require_auth(sess: dict):
    """Check if user is authenticated, redirect to login if not"""
    if not sess.get('authenticated'):
        return RedirectResponse("/", status_code=303)
    return None


def login_user(sess: dict, email: str):
    """Set session for authenticated user"""
    sess['authenticated'] = True
    sess['email'] = email


def logout_user(sess: dict):
    """Clear user session"""
    sess.clear()
