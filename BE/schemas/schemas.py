
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 用户相关模型
class UserCreate(BaseModel):
    username: str
    password: str
    nickName: str = ""
    phoneNum: Optional[int] = None

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    msg: str
    code: int
    token: str

class UserBase(BaseModel):
    nickName: str = ""
    userImg: str = "http://newcoffee.wwp666.cn:10006/assets/default.png"
    userBg: str = "http://newcoffee.wwp666.cn:10006/assets/default_bg.jpg"
    desc: Optional[str] = ""
    vip: int = 0

class FindMyResponse(BaseModel):
    msg: str
    code: str
    result: List[UserBase]

# 商品分类相关模型
class ProductTypeBase(BaseModel):
    id: int
    type: str
    typeDesc: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class TypeResponse(BaseModel):
    result: List[ProductTypeBase]
    code: int

# 商品相关模型
class ProductBase(BaseModel):
    id: int
    pid: str
    type: str
    name: str
    price: float  # 修改为float类型
    desc: str
    smallImg: str
    largeImg: str
    typeDesc: str
    isHot: int
    enname: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

    @property
    def price_str(self) -> str:
        return f"{self.price:.2f}"

class TypeProductsResponse(BaseModel):
    result: List[ProductBase]
    code: int

# 商品详情相关模型
class ProductDetail(BaseModel):
    pid: str
    type: str
    enname: str
    desc: str
    name: str
    price: str
    small_img: str
    large_img: str
    is_hot: int
    type_desc: str
    tem: str = ""
    tem_desc: str = ""
    milk: str = ""
    milk_desc: str = ""
    sugar: str = ""
    sugar_desc: str = ""
    cream: str = ""
    cream_desc: str = ""

    class Config:
        from_attributes = True

class ProductDetailResponse(BaseModel):
    msg: str
    code: int
    result: List[ProductDetail]

# 推广内容相关模型
class PromotionBase(BaseModel):
    imgUrl: str
    desc: str

class SearchGuessResponse(BaseModel):
    data: List[PromotionBase]

# 通用响应模型
class Message(BaseModel):
    detail: str