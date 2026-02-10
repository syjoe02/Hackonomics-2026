from django.conf import settings
from google import genai

from user_calendar.application.ports.external.calendar_advisor import (
    CalendarAdvisorPort,
)


class GeminiCalendarAdvisorAdapter(CalendarAdvisorPort):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def analyze_events(self, events_text: str, document_text: str) -> str:
        prompt = f"""
        USER EVENTS (JSON ARRAY):
        {events_text}

        NEW DOCUMENT:
        {document_text}

        TASK:
        - Analyze how this document might impact the user's events.
        - For relevant events, suggest whether the user should:
          - keep the event as is
          - move it earlier
          - move it later
        - Return a JSON array like this:

        [
          {{
            "event_id": "8f3a2c1e-...",
            "event_title": "Gas Station",
            "suggestion": "move earlier",
            "reason": "Because fuel prices are expected to rise..."
          }}
        ]
        """

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        return response.text
