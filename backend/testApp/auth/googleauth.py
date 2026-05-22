import urllib.parse
from config import settings


def generate_url():
    
    query_params = {
        "client_id": settings.auth_jwt.google_client_id,
        "redirect_uri": "http://localhost:3000",
        "response_type": "code",
        "scope": " ".join([
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
            "profile",
            "email",
        ]),
        "access_type": "offline",
        "prompt": "consent",
    }

    query_string = urllib.parse.urlencode(query_params)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"