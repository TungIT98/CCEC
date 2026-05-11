"""Chat router — RAG-augmented climate AI."""
import uuid
import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from models.schemas import ChatRequest
from services.ai import ai_service
from routers.auth import get_current_user
from services.rag import build_system_prompt, retrieve_climate_context

BASE_SYSTEM_PROMPT = (
    "You are a climate expert assistant for the CCEC Climate Platform. "
    "Answer questions about climate change, carbon markets, Vietnam climate policy, "
    "emissions data, and related topics. Be concise, accurate, and helpful. "
    "When referencing data, mention its source and limitations."
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(
    payload: ChatRequest,
    _current_user=Depends(get_current_user),
):
    """Non-streaming chat — RAG-augmented."""
    conversation_id = payload.conversation_id or str(uuid.uuid4())[:8]

    # Build RAG-augmented system prompt for this query
    system_prompt = build_system_prompt(payload.message)

    message = await ai_service.chat(payload.message, system_prompt=system_prompt)
    from models.schemas import ChatResponse
    return ChatResponse(message=message, conversation_id=conversation_id, sources=[])


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    _current_user=Depends(get_current_user),
):
    """SSE streaming chat — RAG-augmented, token-by-token."""
    conversation_id = payload.conversation_id or str(uuid.uuid4())[:8]

    # Build RAG-augmented system prompt
    system_prompt = build_system_prompt(payload.message)

    async def event_generator():
        yield json.dumps({
            "event": "start",
            "conversation_id": conversation_id,
            "sources": retrieve_climate_context(payload.message),
        })

        try:
            async for chunk in ai_service.stream_chat(payload.message, system_prompt=system_prompt):
                yield json.dumps({"event": "token", "data": chunk})
        except Exception as e:
            yield json.dumps({"event": "error", "error": str(e)})

        yield json.dumps({"event": "done"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )