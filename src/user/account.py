"""
User Account Management
"""

import hashlib
import time
import uuid
from utils import log


def create_salt():
    """Generate and return a salt"""
    return uuid.uuid4().hex


def hash_password(password, salt):
    """Hash a password with a salt and return the result"""
    log.debug('FUNC hash_password(password=%s, salt=%s)', password, salt)
    return hashlib.sha512(salt.encode('cp1252') + password.encode('cp1252')).digest()


def validate_password(password, pwhash, salt):
    """Compare a plaintext password against a hash/salt"""
    log.debug('password=%s, pwhash=%s, salt=%s', password, pwhash, salt)
    attempt = hash_password(password, salt)
    if attempt == hash:
        return True
    else:
        return False


def create_account(username, password):
    """Initialize an account structure for a new player"""
    now = int(time.time())
    salt = create_salt()
    pwhash = hash_password(password=password, salt=salt)
    account = {
        'username': username,
        'email': '',
        'hash': pwhash,
        'salt': salt,
        'active': 0,
        'playing': '',
        'banned': 0,
        'created': now,
        'last_login': now,
        'logins': 1,
        'failures': 0
    }
    return account
