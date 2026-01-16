import urllib.parse
import requests

from django.conf import settings

class GoogleOAuthAdapter:
    AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

    def build_login_url(self) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "access_type": "offline",
            "prompt": "consent",
        }
        query = urllib.parse.urlencode(params)
        return f"{self.AUTH_BASE_URL}?{query}"
    
    def exchange_code_for_token(self, code: str) -> dict:
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        }
        res = requests.post(self.TOKEN_URL, data=data, timeout=5)
        res.raise_for_status()
        return res.json()
    
    def get_userinfo(self, access_token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        res = requests.get(self.USERINFO_URL, headers=headers, timeout=5)
        res.raise_for_status()
        return res.json(0)