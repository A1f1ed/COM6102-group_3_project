from typing import Optional
import redis
from config import REDIS_URL

class RedisConfig:
    _instance = None
    _redis_client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._redis_client:
            self._redis_client = redis.from_url(
                REDIS_URL,
                decode_responses=True  # 自动解码响应
            )

    @property
    def client(self) -> redis.Redis:
        return self._redis_client

# 创建Redis客户端单例
redis_client = RedisConfig().client

# 缓存键前缀
CACHE_KEY_PREFIX = "coffee_shop:"

# 缓存时间（秒）
CACHE_TIMES = {
    "PRODUCT_TYPES": 3600 * 24,  # 商品分类缓存1天
    "PRODUCT_DETAIL": 3600 * 12,  # 商品详情缓存12小时
    "PROMOTIONS": 3600 * 6,      # 推广内容缓存6小时
    "USER": 3600 * 2,            # 用户信息缓存2小时
}

# 缓存键模板
CACHE_KEYS = {
    "PRODUCT_TYPES": CACHE_KEY_PREFIX + "product_types",
    "PRODUCT_DETAIL": CACHE_KEY_PREFIX + "product:{}",  # 需要format商品pid
    "PROMOTIONS": CACHE_KEY_PREFIX + "promotions",
    "USER": CACHE_KEY_PREFIX + "user:{}"  # 需要format用户id
}