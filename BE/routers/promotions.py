from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.models import Promotion
from schemas.schemas import SearchGuessResponse, PromotionBase
from redis_utils import RedisUtils

router = APIRouter(
    prefix="/promotions",
    tags=["推广"]
)

@router.get("/searchguess", response_model=SearchGuessResponse)
async def get_search_guess(db: Session = Depends(get_db)):
    """
    获取推广内容列表
    """
    # 尝试从缓存获取
    cached_promotions = await RedisUtils.get_promotions()
    if cached_promotions:
        return {
            "data": [
                PromotionBase(
                    imgUrl=promo["imgUrl"],
                    desc=promo["desc"]
                ) for promo in cached_promotions
            ]
        }

    # 缓存未命中，从数据库获取
    promotions = db.query(Promotion).order_by(Promotion.sort_order).all()
    
    promotion_list = []
    for promo in promotions:
        promo_data = {
            "imgUrl": promo.imgUrl,
            "desc": promo.desc
        }
        promotion_list.append(promo_data)
    
    # 设置缓存
    await RedisUtils.set_promotions(promotion_list)
    
    return {
        "data": [
            PromotionBase(
                imgUrl=promo["imgUrl"],
                desc=promo["desc"]
            ) for promo in promotion_list
        ]
    }

# 添加缓存清理的辅助函数
async def clear_promotions_cache():
    """
    清理推广内容缓存
    """
    await RedisUtils.clear_promotions_cache()

# 添加更新推广内容的辅助函数
async def update_promotion(db: Session, promotion_id: int, data: dict):
    """
    更新推广内容并清理缓存
    """
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="推广内容不存在")
    
    for key, value in data.items():
        setattr(promotion, key, value)
    
    try:
        db.commit()
        # 更新后清理缓存
        await clear_promotions_cache()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return promotion

# 添加新增推广内容的辅助函数
async def create_promotion(db: Session, data: dict):
    """
    创建新的推广内容并清理缓存
    """
    promotion = Promotion(**data)
    
    try:
        db.add(promotion)
        db.commit()
        db.refresh(promotion)
        # 创建后清理缓存
        await clear_promotions_cache()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return promotion

# 添加删除推广内容的辅助函数
async def delete_promotion(db: Session, promotion_id: int):
    """
    删除推广内容并清理缓存
    """
    promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="推广内容不存在")
    
    try:
        db.delete(promotion)
        db.commit()
        # 删除后清理缓存
        await clear_promotions_cache()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))