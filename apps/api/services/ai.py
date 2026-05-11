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

    async def chat(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Send a chat message (non-streaming)."""
        result = []
        async for chunk in self.stream_chat(message, model=model, system_prompt=system_prompt):
            result.append(chunk)
        return "".join(result)

    async def stream_chat(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ):
        """Stream chat tokens — yields str chunks."""
        if system_prompt is None:
            from routers.chat import BASE_SYSTEM_PROMPT as _sp
            system_prompt = _sp

        try:
            stream = await self.client.chat.completions.create(
                model=model or settings.MINIMAX_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=1024,
                stream=True,
            )
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"[AI unavailable: {type(e).__name__}] Demo mode."


ai_service = AIService()