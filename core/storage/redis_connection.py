import os

import redis.asyncio as redis

from dotenv import load_dotenv
load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_STORAGE_PREFIX = os.getenv("REDIS_STORAGE_PREFIX")


def init_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        username=REDIS_USER,
        password=REDIS_PASSWORD,
        db=REDIS_DB,
    )


redis_client = init_redis_connection()
