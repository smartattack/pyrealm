"""
User Account Management
"""

import hashlib
import uuid
import logging



def create_salt():
    """Generate and return a salt"""
    return uuid.uuid4().hex


def hash_password(password, salt):
    """Hash a password with a salt and return the result"""
    return hashlib.sha512(salt + password).digest()


def validate_password(password, hash, salt):
    """Compare a plaintext password against a hash/salt"""
    attempt = hash_password(password, salt)
    if attempt == hash:
        return True
    else:
        return False


def create_account():
