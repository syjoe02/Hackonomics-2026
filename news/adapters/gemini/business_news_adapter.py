import logging
import time
from datetime import date
from typing import Dict, List

from django.conf import settings
from google import genai
from google.genai import types

from common.ai.json_cleaner import clean_json_response
from common.ai.response_validator import validate_news_items
from news.application.ports.business_news_port import BusinessNewsPort

logger = logging.getLogger(__name__)


class GeminiBusinessNewsAdapter(BusinessNewsPort):
    MODEL = "gemini-2.5-flash-lite"
    MAX_RETRIES = 3
    INITIAL_DELAY = 3

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_country_news(self, country_code: str) -> List[Dict[str, str]]:

        today = date.today().strftime("%Y.%m.%d")
        prompt = f"""
        Act as a senior financial analyst. And Today's date is {today}.

        Summarize the MOST IMPORTANT business and market-moving
        developments from the LAST 72 HOURS affecting:

        • {country_code}
        • the global economy

        REQUIREMENTS:
        - Focus ONLY on developments from the past 72 hours.
        - Prioritize market impact, corporate activity, policy moves,
        financial markets, commodities, and major economic data releases.
        - Do NOT include older trends or background context.
        - If no major developments exist, return [].

        Return EXACTLY 5 high-impact insights.

        Each insight MUST include:
        - a concise, informative title (DO NOT include dates)
        - a clear explanation of the economic or market impact

        Return ONLY a valid JSON array in this format:

        [
        {{
            "title": "...",
            "description": "..."
        }}
        ]
        """

        config = types.GenerateContentConfig(temperature=0.2)
        delay = self.INITIAL_DELAY

        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(f"🌍 Gemini request start → {country_code}")
                response = self.client.models.generate_content(
                    model=self.MODEL,
                    contents=prompt,
                    config=config,
                )

                raw = response.text or ""
                logger.debug(f"Gemini RAW response:\n{raw}")

                if not isinstance(raw, str):
                    raw = str(raw)

                cleaned = clean_json_response(raw)
                logger.debug(f"Cleaned JSON:\n{cleaned}")

                validated = validate_news_items(cleaned)
                logger.debug(f"Validated items: {validated}")

                if validated:
                    logger.info(f"✅ Gemini success → {len(validated)} items")
                    print(validated)
                    return validated

                logger.warning("⚠️ Gemini returned empty or invalid structure")

            except Exception as e:
                logger.exception(f"❌ Gemini error attempt {attempt+1}: {e}")

                if "429" in str(e) or "503" in str(e):
                    if attempt < self.MAX_RETRIES - 1:
                        time.sleep(delay)
                        delay *= 2
                        continue
                break
        logger.error("🚨 Gemini failed after retries")
        return []
