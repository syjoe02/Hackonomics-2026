import time
from typing import Dict, List

from django.conf import settings
from google import genai
from google.genai import types

from common.ai.json_cleaner import clean_json_response
from common.ai.response_validator import validate_news_items
from news.application.ports.business_news_port import BusinessNewsPort


class GeminiBusinessNewsAdapter(BusinessNewsPort):
    MODEL = "gemini-2.5-flash-lite"

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_country_news(self, country_code: str) -> List[Dict[str, str]]:

        prompt = f"""
        Act as a senior financial analyst.

        Summarize the most important global business, market
        and economic developments affecting:

        • {country_code}
        • the global

        Return exactly 5 high-impact insights.

        Each insight must include:
        - a short title
        - a concise explanation of economic impact

        Return ONLY a valid JSON array:

        [
        {{
            "title": "...",
            "description": "..."
        }}
        ]
        """

        config = types.GenerateContentConfig(
            temperature=0.2,
        )

        retries = 3
        delay = 3

        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.MODEL,
                    contents=prompt,
                    config=config,
                )

                raw = response.text

                if not isinstance(raw, str):
                    raw = str(raw)

                cleaned = clean_json_response(raw)
                validated = validate_news_items(cleaned)
                if validated:
                    return validated

                print("⚠️ Gemini returned invalid structure", flush=True)

            except Exception as e:
                print("⚠️ Gemini error:", str(e), flush=True)

                if "429" in str(e) or "503" in str(e):
                    if attempt < retries - 1:
                        time.sleep(delay)
                        delay *= 2
                        continue
                break

        return []
