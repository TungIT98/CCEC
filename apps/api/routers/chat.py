from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional

from models.schemas import ChatRequest, ChatResponse
from services.ai import ai_service
from routers.auth import get_current_user
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    _current_user=Depends(get_current_user),
):
    conversation_id = payload.conversation_id or str(uuid.uuid4())[:8]
    message = await ai_service.chat(payload.message)
    return ChatResponse(message=message, conversation_id=conversation_id, sources=[])
