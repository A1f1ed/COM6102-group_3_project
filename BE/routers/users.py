from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.models import User
from schemas.schemas import FindMyResponse, UserBase
from routers.auth import get_current_user
from redis_utils import RedisUtils

router = APIRouter(
    prefix="/users",
    tags=["用户"],
    responses={401: {"description": "未授权访问"}}
)

@router.get("/findMy", response_model=FindMyResponse)
async def find_my(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的信息
    """
    # 尝试从缓存获取用户信息
    cached_user = await RedisUtils.get_user(current_user.id)
    if cached_user:
        return {
            "msg": "查询我的成功",
            "code": "A001",
            "result": [UserBase(**cached_user)]
        }

    # 构建用户信息
    user_data = {
        "nickName": current_user.nickName or "",
        "userImg": current_user.userImg or "http://newcoffee.wwp666.cn:10006/assets/default.png",
        "userBg": current_user.userBg or "http://newcoffee.wwp666.cn:10006/assets/default_bg.jpg",
        "desc": current_user.desc or "",
        "vip": current_user.vip or 0
    }
    
    # 设置缓存
    await RedisUtils.set_user(current_user.id, user_data)
    
    return {
        "msg": "查询我的成功",
        "code": "A001",
        "result": [UserBase(**user_data)]
    }

# 添加更新用户信息的辅助函数
async def update_user_info(db: Session, user_id: int, data: dict):
    """
    更新用户信息并清理缓存
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户信息
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    try:
        db.commit()
        # 清理用户缓存
        await RedisUtils.clear_user_cache(user_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return user

# 添加用户注销的辅助函数
async def delete_user(db: Session, user_id: int):
    """
    删除用户并清理缓存
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    try:
        db.delete(user)
        db.commit()
        # 清理用户缓存
        await RedisUtils.clear_user_cache(user_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 添加批量清理用户缓存的辅助函数
async def clear_all_user_caches():
    """
    清理所有用户缓存（在需要时使用，如系统维护）
    """
    # 使用Redis的模式匹配删除所有用户缓存
    pattern = "coffee_shop:user:*"
    keys = RedisUtils.redis_client.keys(pattern)
    if keys:
        RedisUtils.redis_client.delete(*keys)