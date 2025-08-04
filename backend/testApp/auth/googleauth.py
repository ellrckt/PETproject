import urllib.parse
import secrets

from .state_storage import state_storage
from config import settings

def generate_url():
    random_state = secrets.token_urlsafe(16)
    state_storage.add(random_state)

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
        "state": random_state,
    }

    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"