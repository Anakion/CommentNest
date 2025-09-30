from redis.asyncio import Redis
from dataclasses import dataclass


@dataclass
class CacheComments:
    redis_cache: Redis

    async def get(self, key: str):
        return await self.redis_cache.get(key)

    async def set(self, key: str, value: str, expire: int = 60):
        await self.redis_cache.set(key, value, ex=expire)

    async def delete(self, key: str):
        await self.redis_cache.delete(key)
