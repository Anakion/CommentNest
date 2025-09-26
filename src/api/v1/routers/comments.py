from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from src.dependecy import get_comment_service
from src.schemas.comment import CommentCreateSchema, CommentResponseSchema
from src.services.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentResponseSchema)
async def create_comment(
    payload: CommentCreateSchema,
    service: Annotated[CommentService, Depends(get_comment_service)],
):
    return await service.create_comment(payload)


@router.get("/", response_model=List[CommentResponseSchema])
async def list_comments(
    service: Annotated[CommentService, Depends(get_comment_service)],
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(25, ge=1, le=100, description="Comments per page"),
    sort_by: str = Query(
        "created_at", description="Sort by field: created_at, user_name, email"
    ),
    order: str = Query("desc", description="Order: asc or desc"),
):
    return await service.list_comments(
        page=page, per_page=per_page, sort_by=sort_by, order=order
    )


@router.get("/with-replies", response_model=List[CommentResponseSchema])
async def list_comments_with_replies(
    service: Annotated[CommentService, Depends(get_comment_service)],
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    return await service.list_comments_with_replies(
        page=page, per_page=per_page, sort_by=sort_by, order=order
    )
