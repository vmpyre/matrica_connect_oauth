# OAuth2 Configuration
REDIRECT_URI = "http://localhost:8000/callback"  
AUTHORIZE_URL = "https://matrica.io/oauth2"
API_ENDPOINT = "https://api.matrica.io/oauth2"

TOKEN_URL = f"{API_ENDPOINT}/token/"
USER_WALLETS_URL = f"{API_ENDPOINT}/user/wallets"

SCOPES = "wallets"  