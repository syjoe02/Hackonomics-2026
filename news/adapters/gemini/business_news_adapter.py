import time

from django.conf import settings
from google import genai
from google.genai import types

from news.application.ports.business_news_port import BusinessNewsPort


class GeminiBusinessNewsAdapter(BusinessNewsPort):
    MODEL = "gemini-2.5-flash-lite"

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_country_news(self, country_code: str) -> str:

        prompt = f"""
            You are a financial analyst.

            Summarize IMPORTANT business & economic news from the LAST 3 DAYS affecting {country_code}.

            Include global events only if they impact this country.

            Focus on:
            - inflation & consumer prices
            - interest rates
            - fuel & energy costs
            - housing & employment
            - technology, exports & markets

            Return concise bullet points explaining what happened and why it matters.
        """

        config = types.GenerateContentConfig(
            tools=[{"url_context": {}}],
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
                return response.text.strip()

            except Exception as e:
                if "429" in str(e) or "503" in str(e):
                    if attempt < retries - 1:
                        time.sleep(delay)
                        delay *= 2
                        continue
                raise e

        return "News temporarily unavailable."
