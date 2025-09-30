from redis.asyncio import Redis

from src.core.config import settings
from src.utils.redis_client import CacheComments

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)
cache_comments = CacheComments(redis_cache=redis_client)
