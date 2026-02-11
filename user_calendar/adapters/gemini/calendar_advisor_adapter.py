import time

from django.conf import settings
from google import genai
from google.genai import types

from user_calendar.application.ports.external.calendar_advisor import (
    CalendarAdvisorPort,
)


class GeminiCalendarAdvisorAdapter(CalendarAdvisorPort):
    MAX_EVENTS = 10
    MODEL_NAME = "gemini-2.5-flash-lite"

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def analyze_events(
        self,
        events_text: str,
        document_text: str,
        country_context: str,
    ) -> str:

        events_lines = events_text.split("\n")
        events_preview = "\n".join(events_lines[: self.MAX_EVENTS])

        prompt = f"""
        COUNTRY CONTEXT: {country_context}
        USER EVENTS: {events_preview}
        NEW DOCUMENT/URL: {document_text}

        ASK:
        - Analyze how this document/news impacts the user's events.
        - Return a JSON array of suggestions.
        """

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        )

        max_retries = 3
        delay = 5

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.MODEL_NAME,
                    contents=prompt,
                    config=config,
                )
                return response.text

            except Exception as e:
                if "429" in str(e) or "503" in str(e):
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= 2
                        continue
                raise e

        return "[]"
