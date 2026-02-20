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
        You are a financial news analyst.

        TASK:
        1. Collect IMPORTANT business & economic news from the LAST 3 DAYS.
        2. Focus on country: {country_code}
        3. Include global news only if it impacts this country.
        4. Summarize into clear bullet points.

        Focus on:
        - inflation
        - interest rates
        - fuel/energy prices
        - housing market
        - employment
        - technology & exports
        - stock market
        - consumer costs

        OUTPUT:
        bullet points only.
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
