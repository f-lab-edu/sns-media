import redis

redis_client = redis.Redis(
    host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True
)
