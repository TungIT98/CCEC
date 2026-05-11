"""RAG (Retrieval-Augmented Generation) search endpoints."""
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Literal

from services.rag import retrieve_climate_context, build_rag_context
from routers.auth import get_current_user

router = APIRouter(prefix="/ai/search", tags=["ai-search"])


class SearchResponse(BaseModel):
    query: str
    top_k: int
    chunks: list[str]
    count: int


@router.get("/rag", response_model=SearchResponse)
async def rag_search(
    q: str = Query(..., description="Search query for climate KB"),
    k: int = Query(default=4, ge=1, le=10, description="Number of chunks to retrieve"),
    _: None = Depends(get_current_user),
):
    """Retrieve top-k climate KB chunks for a query (RAG step 1)."""
    chunks = retrieve_climate_context(q, k=k)
    return SearchResponse(
        query=q,
        top_k=k,
        chunks=chunks,
        count=len(chunks),
    )


@router.get("/rag/context", response_model=SearchResponse)
async def rag_context(
    q: str = Query(..., description="Search query"),
    k: int = Query(default=4, ge=1, le=10),
    _: None = Depends(get_current_user),
):
    """Build full RAG-augmented system prompt context string for a query."""
    system_prompt = build_rag_context(q, k=k)
    chunks = retrieve_climate_context(q, k=k)
    return SearchResponse(
        query=q,
        top_k=k,
        chunks=[system_prompt] if system_prompt else [],
        count=len(chunks),
    )