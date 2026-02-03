import google_auth_oauthlib.flow
from django.conf import settings


def build_google_calendar_flow(state=None):
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CALENDAR_CLIENT_ID,
            "client_secret": settings.GOOGLE_CALENDAR_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_CALENDAR_REDIRECT_URI],
        }
    }

    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/calendar"],
        state=state,
    )

    flow.redirect_uri = settings.GOOGLE_CALENDAR_REDIRECT_URI
    return flow