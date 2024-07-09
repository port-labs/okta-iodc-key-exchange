## A helper function to generate a PKCE code verifier and challenge
## for OAuth2.0 authorization code flow with PKCE extension.


import hashlib
import os
import base64
import secrets


def generate_code_verifier() -> str:
    """Generates a code verifier for PKCE."""
    return base64.urlsafe_b64encode(os.urandom(36)).decode().rstrip('=')

def generate_code_challenge(verifier: str) -> str:
    """Generates a code challenge for PKCE."""
    sha256 = hashlib.sha256()
    sha256.update(verifier.encode())
    return base64.urlsafe_b64encode(sha256.digest()).decode().rstrip('=')

def generate_pkce_params() -> dict:
    """Generates a code verifier and challenge for PKCE."""
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    return {'code_verifier': verifier, 'code_challenge': challenge}

def generate_state() -> str:
    """Generates a state value for OAuth2.0 authorization request."""
    return secrets.token_urlsafe(32)

def generate_nonce() -> str:
    """Generates a nonce value for OpenID Connect authentication request."""
    return secrets.token_urlsafe(32)
