from typing import List
from fastapi import APIRouter, Depends, HTTPException
from opentelemetry import trace

from app.schemas.prompt_store import PromptStoreResponse
from app.services.prompt_store_service import PromptStoreService

router = APIRouter()

tracer = trace.get_tracer(__name__)

@router.get("/", response_model=List[PromptStoreResponse])
async def get_prompt_store_list(service: PromptStoreService = Depends()):
    logs = await service.list_prompt_store()
    return [log.to_response() for log in logs]

@router.get("/{prompt_store_id}", response_model=PromptStoreResponse)
async def get_prompt_store(prompt_store_id: str, service: PromptStoreService = Depends()):
    log = await service.get_prompt_store(prompt_store_id)
    if not log:
        raise HTTPException(status_code=404, detail="PromptStore not found")
    return log.to_response()