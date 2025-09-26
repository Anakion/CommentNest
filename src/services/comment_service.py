from dataclasses import dataclass

from fastapi import HTTPException

from src.core.config import Settings
from src.models.comment import Comments
from src.repositories.comment_repo import CommentRepository
from src.schemas.comment import CommentCreateSchema


@dataclass
class CommentService:
    repository: CommentRepository
    settings: Settings

    async def create_comment(self, comment: CommentCreateSchema) -> Comments:
        # Если user_name пустой или состоит только из пробелов
        if not comment.user_name or not comment.user_name.strip():
            raise HTTPException(status_code=400, detail="User name is required")

        # Если текст пустой или состоит только из пробелов
        if not comment.text.strip():
            raise HTTPException(status_code=400, detail="Text is required")

        if comment.parent_id:
            # Получаем родительский комментарий из репозитория
            parent_comment = await self.repository.get_comment_by_id(comment.parent_id)
            # Если такого комментария нет
            if not parent_comment:
                raise HTTPException(status_code=404, detail="Parent comment not found")

        try:
            return await self.repository.create_comment(comment)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def list_comments(
        self,
        page: int = 1,
        per_page: int = 25,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> list[Comments]:
        skip = (page - 1) * per_page
        return await self.repository.get_comments(
            skip=skip, limit=per_page, sort_by=sort_by, order=order
        )

    async def list_comments_with_replies(
        self,
        page: int = 1,
        per_page: int = 25,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> list[Comments]:
        skip = (page - 1) * per_page
        roots = await self.repository.get_comments(
            skip=skip, limit=per_page, sort_by=sort_by, order=order
        )

        # для каждого корневого комментария подтягиваем ответы рекурсивно
        for root in roots:
            root.replies = await self.repository.get_replies(root.id)
        return roots
