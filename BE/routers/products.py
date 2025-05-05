
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json

from database import get_db
from models.models import ProductType, Product
from schemas.schemas import (
    TypeResponse, 
    TypeProductsResponse, 
    ProductDetailResponse
)
from redis_utils import RedisUtils

router = APIRouter(
    prefix="/products",
    tags=["商品"]
)

class ProductService:
    """商品服务类，处理商品相关的业务逻辑和缓存管理"""
    
    @staticmethod
    async def get_product_types(db: Session) -> List[Dict[str, Any]]:
        """获取所有商品分类"""
        # 尝试从缓存获取
        cached_types = await RedisUtils.get_cache("coffee_shop:product_types")
        if cached_types:
            return cached_types

        # 从数据库获取
        types = db.query(ProductType).all()
        types_data = [
            {
                "id": t.id,
                "type": t.type,
                "typeDesc": t.typeDesc,
                "createdAt": t.createdAt.isoformat(),
                "updatedAt": t.updatedAt.isoformat()
            }
            for t in types
        ]
        
        # 设置缓存
        await RedisUtils.set_cache("coffee_shop:product_types", types_data)
        return types_data

    @staticmethod
    async def get_product_detail(db: Session, pid: str) -> Dict[str, Any]:
        """获取商品详情"""
        cache_key = f"coffee_shop:product:detail:{pid}"
        
        # 尝试从缓存获取
        cached_product = await RedisUtils.get_cache(cache_key)
        if cached_product:
            return cached_product

        # 从数据库获取
        product = db.query(Product).filter(Product.pid == pid).first()
        if not product:
            raise HTTPException(status_code=404, detail="商品不存在")
        
        # 获取商品类型描述
        type_desc = await ProductService.get_type_desc(db, product.type)
        
        # 格式化商品详情
        product_detail = {
            "pid": product.pid,
            "type": product.type,
            "enname": product.enname,
            "desc": product.desc,
            "name": product.name,
            "price": f"{float(product.price):.2f}",
            "small_img": product.smallImg,
            "large_img": product.largeImg,
            "is_hot": product.isHot,
            "type_desc": type_desc,
            "tem": product.tem or "",
            "tem_desc": product.tem_desc or "",
            "milk": product.milk or "",
            "milk_desc": product.milk_desc or "",
            "sugar": product.sugar or "",
            "sugar_desc": product.sugar_desc or "",
            "cream": product.cream or "",
            "cream_desc": product.cream_desc or ""
        }
        
        # 设置缓存
        await RedisUtils.set_cache(cache_key, product_detail)
        return product_detail

    @staticmethod
    async def get_type_desc(db: Session, type_name: str) -> str:
        """获取商品类型描述"""
        cached_types = await RedisUtils.get_cache("coffee_shop:product_types")
        if cached_types:
            for t in cached_types:
                if t["type"] == type_name:
                    return t["typeDesc"]
        
        product_type = db.query(ProductType).filter(ProductType.type == type_name).first()
        return product_type.typeDesc if product_type else ""

@router.get("/type", response_model=TypeResponse)
async def get_product_types(db: Session = Depends(get_db)):
    """获取所有商品分类"""
    try:
        types_data = await ProductService.get_product_types(db)
        return {
            "result": types_data,
            "code": 400
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取商品分类失败: {str(e)}"
        )

@router.get("/typeProducts/{type_name}", response_model=TypeProductsResponse)
async def get_type_products(
    type_name: str,
    db: Session = Depends(get_db)
):
    """获取指定分类的商品列表"""
    try:
        # 尝试从缓存获取商品列表
        cache_key = f"coffee_shop:product:type:{type_name}"
        cached_products = await RedisUtils.get_cache(cache_key)
        
        if cached_products:
            return {
                "result": cached_products,
                "code": 500
            }
        
        # 从数据库获取商品列表
        products = db.query(Product).filter(Product.type == type_name).all()
        result_products = []
        
        # 获取商品类型描述
        type_desc = await ProductService.get_type_desc(db, type_name)
        
        for product in products:
            product_data = {
                "id": product.id,
                "pid": product.pid,
                "type": product.type,
                "name": product.name,
                "price": float(product.price),
                "desc": product.desc,
                "smallImg": product.smallImg,
                "largeImg": product.largeImg,
                "typeDesc": type_desc,
                "isHot": product.isHot,
                "enname": product.enname,
                "createdAt": product.createdAt.isoformat(),
                "updatedAt": product.updatedAt.isoformat()
            }
            result_products.append(product_data)
        
        # 设置缓存，过期时间30分钟
        await RedisUtils.set_cache(cache_key, result_products, expire=1800)
        
        return {
            "result": result_products,
            "code": 500
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取商品列表失败: {str(e)}"
        )

@router.get("/productDetail/{pid}", response_model=ProductDetailResponse)
async def get_product_detail(pid: str, db: Session = Depends(get_db)):
    """获取商品详情"""
    try:
        product_detail = await ProductService.get_product_detail(db, pid)
        return {
            "msg": "查询商品详情成功",
            "code": 600,
            "result": [product_detail]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取商品详情失败: {str(e)}"
        )