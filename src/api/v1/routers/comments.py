import json
from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from src.dependecy import get_comment_service, get_comment_cache_service
from src.schemas.comment import CommentCreateSchema, CommentResponseSchema
from src.services.comment_cache_service import CommentCacheService
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
    cache_service: Annotated[CommentCacheService, Depends(get_comment_cache_service)],
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(25, ge=1, le=100, description="Comments per page"),
    sort_by: str = Query(
        "created_at", description="Sort by field: created_at, user_name, email"
    ),
    order: str = Query("desc", description="Order: asc or desc"),
):
    # Пробуем достать из кэша
    cached = await cache_service.get_comments_list_page(page, per_page, sort_by, order)
    if cached:
        print("cached")
        return json.loads(cached)

    # Если кэш пустой, достаем из сервиса
    comments = await service.list_comments(page, per_page, sort_by, order)

    # Сериализуем SQLAlchemy объекты через Pydantic
    comments_serialized = [
        CommentResponseSchema.model_validate(c).model_dump(mode="json")
        for c in comments
    ]

    # Сохраняем результат в Redis
    await cache_service.set_comments_list_page(
        page, per_page, sort_by, order, json.dumps(comments_serialized)
    )

    # Возвращаем результат
    return comments_serialized


@router.get("/with-replies", response_model=List[CommentResponseSchema])
async def list_comments_with_replies(
    service: Annotated[CommentService, Depends(get_comment_service)],
    cache_service: Annotated[CommentCacheService, Depends(get_comment_cache_service)],
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
):
    # Попробуем достать из кэша
    cached = await cache_service.get_comments_page(page, per_page, sort_by, order)
    if cached is not None and cached != "":
        print("ccccccasche")
        return json.loads(cached)

    # Получаем данные из сервиса (репозитория)
    comments = await service.list_comments_with_replies(page, per_page, sort_by, order)
    print("Данные из бд")
    # Сериализуем с конвертацией HttpUrl и datetime
    comments_serialized = [
        CommentResponseSchema.model_validate(c).model_dump(mode="json")
        for c in comments
    ]

    # Сохраняем в Redis
    await cache_service.set_comments_page(
        page, per_page, sort_by, order, json.dumps(comments_serialized)
    )

    # Возвращаем
    return comments_serialized
