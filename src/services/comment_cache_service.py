from dataclasses import dataclass

from src.utils.redis_client import CacheComments


@dataclass
class CommentCacheService:
    redis_cache_service: CacheComments

    # ===== / (список корневых комментариев) =====
    async def get_comments_list_page(
        self, page: int, per_page: int, sort_by: str, order: str
    ):
        key = f"comments:list:page={page}:per_page={per_page}:sort={sort_by}:order={order}"
        return await self.redis_cache_service.get(key)

    async def set_comments_list_page(
        self, page: int, per_page: int, sort_by: str, order: str, data: str
    ):
        key = f"comments:list:page={page}:per_page={per_page}:sort={sort_by}:order={order}"
        await self.redis_cache_service.set(key, data, expire=60)

    # ===== /with-replies (список корневых комментариев с ответами) =====
    async def get_comments_page(
        self, page: int, per_page: int, sort_by: str, order: str
    ):
        key = f"comments:page={page}:per_page={per_page}:sort={sort_by}:order={order}"
        return await self.redis_cache_service.get(key)

    async def set_comments_page(
        self, page: int, per_page: int, sort_by: str, order: str, data: str
    ):
        key = f"comments:page={page}:per_page={per_page}:sort={sort_by}:order={order}"
        await self.redis_cache_service.set(key, data, expire=60)

    # ===== удалить кэш страницы =====
    async def delete_comments_page(
        self, page: int, per_page: int, sort_by: str, order: str
    ):
        key = f"comments:page={page}:per_page={per_page}:sort={sort_by}:order={order}"
        await self.redis_cache_service.delete(key)
