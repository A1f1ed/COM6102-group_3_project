from redis import asyncio as aioredis
from typing import Optional, Any
import json
from config import REDIS_URL
from redis_config import redis_client, CACHE_KEYS, CACHE_TIMES


class RedisUtils:
    redis_client: Optional[aioredis.Redis] = None

    @classmethod
    async def init_redis(cls, app=None):
        """初始化Redis连接"""
        cls.redis_client = await aioredis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )

    @classmethod
    async def close_redis(cls):
        """关闭Redis连接"""
        if cls.redis_client:
            await cls.redis_client.close()

    @classmethod
    async def set_cache(cls, key: str, value: Any, expire: int = 3600):
        """设置缓存，默认过期时间1小时"""
        await cls.redis_client.set(
            key,
            json.dumps(value),
            ex=expire
        )

    @classmethod
    async def get_cache(cls, key: str) -> Optional[Any]:
        """获取缓存"""
        data = await cls.redis_client.get(key)
        return json.loads(data) if data else None

    @classmethod
    async def delete_cache(cls, key: str):
        """删除缓存"""
        await cls.redis_client.delete(key)

    @classmethod
    async def clear_pattern(cls, pattern: str):
        """清理指定模式的所有缓存"""
        cursor = 0
        while True:
            cursor, keys = await cls.redis_client.scan(
                cursor,
                match=pattern,
                count=100
            )
            if keys:
                await cls.redis_client.delete(*keys)
            if cursor == 0:
                break


    @classmethod
    async def batch_update_cache(cls, data: dict):
        """批量更新Redis缓存"""
        pipe = cls.redis_client.pipeline()
        for key, value in data.items():
            pipe.hset(key, mapping=value)
            pipe.expire(key, 3600)  # 设置过期时间
        await pipe.execute()
        
    # 推广相关方法
    @classmethod
    async def get_promotions(cls) -> Optional[Any]:
        """获取推广内容缓存"""
        return await cls.get_cache(CACHE_KEYS["PROMOTIONS"])

    @classmethod
    async def set_promotions(cls, data: Any, expire: int = CACHE_TIMES["PROMOTIONS"]):
        """设置推广内容缓存"""
        await cls.set_cache(CACHE_KEYS["PROMOTIONS"], data, expire)

    @classmethod
    async def clear_promotions_cache(cls):
        """清理推广内容缓存"""
        await cls.delete_cache(CACHE_KEYS["PROMOTIONS"])

    # 用户相关方法
    @classmethod
    async def get_user(cls, user_id: int) -> Optional[Any]:
        """获取用户缓存"""
        return await cls.get_cache(CACHE_KEYS["USER"].format(user_id))

    @classmethod
    async def set_user(cls, user_id: int, data: Any, expire: int = CACHE_TIMES["USER"]):
        """设置用户缓存"""
        await cls.set_cache(CACHE_KEYS["USER"].format(user_id), data, expire)

    @classmethod
    async def clear_user_cache(cls, user_id: int):
        """清理用户缓存"""
        await cls.delete_cache(CACHE_KEYS["USER"].format(user_id))