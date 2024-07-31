from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query
from opentelemetry import trace

from app.schemas.prompt_store import PromptStoreListParams, PromptStoreResponse
from app.services.prompt_store_service import PromptStoreService

router = APIRouter()

tracer = trace.get_tracer(__name__)

@router.get("/", response_model=Dict[str, Any])
async def get_prompt_store_list(
    page: int = Query(1, alias="page"),
    page_size: int = Query(20, alias="page_size"),
    service: PromptStoreService = Depends()):
    filters = PromptStoreListParams(page=page, page_size=page_size)
    result = await service.list_prompt_store(filters)
    return {
        "data": [prompt_store.to_response() for prompt_store in result.get('data')],
        "total": result['total'],
        "page": result['page'],
        "page_size": result['page_size']
    }

@router.get("/{prompt_store_id}", response_model=PromptStoreResponse)
async def get_prompt_store(prompt_store_id: str, service: PromptStoreService = Depends()):
    log = await service.get_prompt_store(prompt_store_id)
    if not log:
        raise HTTPException(status_code=404, detail="PromptStore not found")
    return log.to_response()