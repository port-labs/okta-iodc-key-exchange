## A JWT client for OAuth2.0 authorization code flow with PKCE extension.

import requests
from pkce import generate_pkce_params, generate_state, generate_nonce
from loguru import logger

class JWTClient:

    def __init__(self, client_id: str, token_url: str, authorization_url: str, authorization_scope: list[str],  redirect_uri: str):
        self.client_id = client_id
        self.token_url = token_url
        self.authorization_url = authorization_url
        self.authorization_scope = authorization_scope
        self.redirect_uri = redirect_uri
        self.pkce_params = generate_pkce_params()
    
    def get_authorization_url(self) -> str:
        logger.info("Generating authorization URL")
        state = generate_state()
        nonce = generate_nonce()
        return f"{self.authorization_url}?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={' '.join(self.authorization_scope)}&state={state}&nonce={nonce}&code_challenge={self.pkce_params['code_challenge']}&code_challenge_method=S256"
    
    def get_access_token(self, code: str) -> dict:
        logger.info(f"Getting access token for code: {code}")
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code_verifier': self.pkce_params['code_verifier']
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'cache-control': 'no-cache', 'Accept': 'application/json'}
        try:
            response = requests.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error: {e}")
            return {'error': e.response.text}
