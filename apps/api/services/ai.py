import os
from typing import Optional
from openai import AsyncOpenAI
from core.config import settings


class AIService:
    def __init__(self):
        self._client: Optional[AsyncOpenAI] = None

    @property
    def client(self) -> AsyncOpenAI:
        if self._client is None:
            api_key = settings.MINIMAX_API_KEY or os.environ.get("MINIMAX_API_KEY", "DUMMY_KEY")
            base_url = settings.MINIMAX_BASE_URL
            self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)

        return self._client

    async def chat(self, message: str, model: Optional[str] = None) -> str:
        """Send a chat message to the AI provider."""
        actual_model = model or settings.MINIMAX_MODEL

        system_prompt = (
            "You are a climate expert assistant for the CCEC Climate Platform. "
            "Answer questions about climate change, carbon markets, Vietnam climate policy, "
            "emissions data, and related topics. Be concise, accurate, and helpful. "
            "When referencing data, mention its source and limitations."
        )

        try:
            response = await self.client.chat.completions.create(
                model=settings.MINIMAX_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content or "No response generated."
        except Exception as e:
            return (
                f"[AI service unavailable: {type(e).__name__}] "
                "I'm operating in demo mode. Please configure MINIMAX_API_KEY in .env "
                "(get your key from https://platform.minimax.io)."
            )


ai_service = AIService()
