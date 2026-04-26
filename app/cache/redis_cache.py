import json     
import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# if data is already present in cache 
async def get_cached_prediction(key: str):
    value = await redis_client.get(key)
    if value is not None:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return None
    return None



# if data is not present in cache
async def set_cached_prediction(key: str , value:dict , expiry: int = 3600):
    await redis_client.setex(key, expiry, json.dumps(value))
