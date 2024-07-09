from flask import Flask, request, jsonify, redirect
from loguru import logger
from jwt_client import JWTClient
import os

app = Flask(__name__)

## Load values from environment variables
client_id = os.getenv('OKTA_OIDC_CLIENT_ID')
token_url = os.getenv('OKTA_OIDC_TOKEN_URL')
authorization_url = os.getenv('OKTA_OIDC_AUTHORIZATION_URL')
authorization_scope = os.getenv('OKTA_OIDC_AUTHORIZATION_SCOPE', 'openid').split(',')
redirect_uri = os.getenv('OKTA_OIDC_REDIRECT_URI', 'http://localhost:8080/callback')

client = JWTClient(client_id, token_url, authorization_url, authorization_scope, redirect_uri)

@app.route('/', methods=['POST', 'GET'])
def root_page():
    return {'message': 'Hello, World!'}

@app.route('/login', methods=['GET'])
def authorize():
    return redirect(client.get_authorization_url())

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    if not code:
        logger.error("No authorization code received.")
        return jsonify({'error': 'No authorization code received.'})
    logger.info(f"Received authorization code: {code}, getting access token.")
    return jsonify(client.get_access_token(code))

if __name__ == '__main__':
    app.run(debug=True)