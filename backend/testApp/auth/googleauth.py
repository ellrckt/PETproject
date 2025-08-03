import urllib.parse
from config import settings

def generate_url():
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'scope': "".join([
            'https://www.googleapis.com/auth/userinfo.email'
            # 'openid',
            # 'profile',
            # 'email',
        ]),
        'response_type': 'code',
        'redirect_uri': 'http://localhost:3000/home',
        'client_id': settings.auth_jwt.google_client_id ,
        'access_type': 'offline',
        #state
       }
    query_string = urllib.parse.urlencode(params,quote_via=urllib.parse.quote)
    return f'{base_url}?{query_string}'