import redis

from src import config

redis_client = redis.Redis(
    host=config.redis.host,
    port=config.redis.port,
    db=config.redis.db,
    encoding="utf-8",
    decode_responses=True,
)
