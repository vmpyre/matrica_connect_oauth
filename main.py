import os
import uvicorn
import httpx
import hashlib
import base64
import logging
import secrets
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from config_file import REDIRECT_URI, SCOPES, AUTHORIZE_URL, TOKEN_URL, USER_WALLETS_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Helper function to create a PKCE code challenge
def generate_code_challenge():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return code_verifier, code_challenge

oauth_state = {}

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    state = secrets.token_urlsafe(16)
    code_verifier, code_challenge = generate_code_challenge()
    oauth_state[state] = code_verifier

    authorize_url = f"{AUTHORIZE_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}&state={state}&code_challenge={code_challenge}&code_challenge_method=S256"
    
    return templates.TemplateResponse("index.html", {"request": request, "authorize_url": authorize_url})

@app.get("/callback")
async def callback(request: Request, code: str = None, state: str = None, error: str = None):
    if error == "access_denied":
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "You denied the authorization request."})
        
    code_verifier = oauth_state.pop(state, None)
    if code_verifier is None:
        raise HTTPException(status_code=400, detail="Invalid state")

    token_payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post(TOKEN_URL, data=token_payload)
        if token_response.status_code != 200:
            return templates.TemplateResponse(
                "error.html", 
                {
                    "request": request, 
                    "error_message": "Authorization failed!"
                }
            )

        access_token = token_response.json().get("access_token")

    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        user_response = await client.get(USER_WALLETS_URL, headers=headers)
        if user_response.status_code != 200:
            return templates.TemplateResponse(
                "error.html", 
                {
                    "request": request, 
                    "error_message": f"Failed to fetch user wallets (Error: {user_response.status_code})"
                }
            )

        user_wallets = user_response.json()
    
    if not user_wallets:
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request, 
                "error_message": "No wallets linked to Matrica."
            }
        )
    
    return templates.TemplateResponse(
        "success.html", 
        {
            "request": request, 
            "success_message": user_wallets
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
