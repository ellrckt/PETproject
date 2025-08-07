import urllib.parse
import secrets
from fastapi import Request, HTTPException
# from .state_storage import state_storage
from config import settings
from datetime import datetime,timedelta
def generate_url():
    # random_state = secrets.token_urlsafe(16)
    # state_storage.add(random_state)
    # state_storage[random_state] = datetime.now() + timedelta(minutes=10)
    query_params = {
        "client_id": settings.auth_jwt.google_client_id,
        "redirect_uri": "http://localhost:3000/home",
        "response_type": "code",
        "scope": " ".join([
            'https://www.googleapis.com/auth/userinfo.email',
            "openid",
            "profile",
            "email",
        ]),
        "access_type": "offline",
        # "state": random_state,
    }

    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"

# async def verify_state(request: Request):
#     state = request.query_params.get("state")
#     if not state or state not in state_storage:
#         raise HTTPException(status_code=400, detail="Invalid state parameter")
    
#     if datetime.now() > state_storage[state]:
#         del state_storage[state]
#         raise HTTPException(status_code=400, detail="State expired")
    
#     del state_storage[state]
#     return True