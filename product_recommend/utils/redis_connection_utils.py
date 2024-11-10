# utils/redis_connection.py
import redis

from product_recommend import settings


class RedisConnectionUtils:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RedisConnectionUtils, cls).__new__(cls)
            cls._instance.connection = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB
            )
        return cls._instance

    def get_connection(self):
        return self.connection
