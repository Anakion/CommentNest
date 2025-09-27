from redis.asyncio import Redis
from src.utils.redis_client import CacheComments

redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
cache_comments = CacheComments(redis_cache=redis_client)
