from os import getenv
import redis.asyncio as redis


from dotenv import load_dotenv

load_dotenv()

REDIS_URL = getenv('REDIS_URL')

async def get_redis():
    if not REDIS_URL:
        raise ValueError("REDIS_URL didn't find")
    redis_client = redis.from_url(REDIS_URL, decode_responses=True) #type:ignore
    return redis_client