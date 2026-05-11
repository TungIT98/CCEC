import os
from typing import Optional
import httpx
from openai import AsyncOpenAI

from core.config import settings


class AIService:
    def __init__(self):
        self._client: Optional[AsyncOpenAI] = None

    @property
    def client(self) -> AsyncOpenAI:
        if self._client is None:
            # Primary: Groq
            api_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY", "DUMMY_KEY")
            base_url = settings.OPENAI_BASE_URL
            model = settings.OPENAI_MODEL

            if settings.AI_PROVIDER == "deepseek" and settings.DEEPSEEK_API_KEY:
                api_key = settings.DEEPSEEK_API_KEY
                base_url = settings.DEEPSEEK_BASE_URL
                model = settings.DEEPSEEK_MODEL
            elif settings.AI_PROVIDER == "portkey" and settings.PORTKEY_API_KEY:
                api_key = settings.PORTKEY_API_KEY
                base_url = settings.PORTKEY_BASE_URL
                model = settings.OPENAI_MODEL

            self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)

        return self._client

    async def chat(self, message: str, model: Optional[str] = None) -> str:
        """Send a chat message to the AI provider."""
        actual_model = model or settings.OPENAI_MODEL

        system_prompt = (
            "You are a climate expert assistant for the CCEC Climate Platform. "
            "Answer questions about climate change, carbon markets, Vietnam climate policy, "
            "emissions data, and related topics. Be concise, accurate, and helpful. "
            "When referencing data, mention its source and limitations."
        )

        try:
            response = await self.client.chat.completions.create(
                model=actual_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content or "No response generated."
        except Exception as e:
            # Fallback to mock response if API is unavailable
            return (
                f"[AI service unavailable: {type(e).__name__}] "
                "I'm operating in demo mode. Please configure a valid AI API key in .env "
                "(OPENAI_API_KEY for Groq, DEEPSEEK_API_KEY for DeepSeek, or PORTKEY_API_KEY for PortKey)."
            )


ai_service = AIService()
