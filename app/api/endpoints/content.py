from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.content import ContentCreate, ContentResponse, ContentUpdate
from app.services.content_service import ContentService


router = APIRouter()

@router.post("/", response_model=ContentResponse)
async def create_content(content: ContentCreate, service: ContentService = Depends()):
    content = await service.create_content(content)
    return content.to_response()

@router.get("/", response_model=List[ContentResponse])
async def get_contents(service: ContentService = Depends()):
    content_list = await service.list_content()
    return [content.to_response() for content in content_list]

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str, service: ContentService = Depends()):
    content = await service.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content.to_response()

@router.patch("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: str,
    content: ContentUpdate,
    service: ContentService = Depends()):
    content = await service.update_content(content_id, content)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content.to_response()

@router.delete("/{content_id}", response_model=None)
async def delete_content(content_id: str, service: ContentService = Depends()):
    success = await service.delete_content(content_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"detail": "Content deleted successfully"}