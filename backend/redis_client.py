from typing import Optional

import redis.asyncio as redis

from config import get_settings

_client: Optional[redis.Redis] = None


async def get_async_redis_client() -> redis.Redis:
    # Constructing redis.asyncio.Redis requires a running event loop, so this
    # must stay a coroutine (FastAPI awaits it in-loop via Depends) rather
    # than a plain function, which FastAPI would run in a worker thread.
    global _client
    if _client is None:
        settings = get_settings()
        _client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    return _client
