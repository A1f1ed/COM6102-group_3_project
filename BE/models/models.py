
from sqlalchemy import Column, Integer, String, DECIMAL, Text, DATETIME, ForeignKey, Enum, BOOLEAN
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nickName = Column(String(50), default='')
    phoneNum = Column(Integer)
    userImg = Column(String(255), default='http://newcoffee.wwp666.cn:10006/assets/default.png')
    userBg = Column(String(255), default='http://newcoffee.wwp666.cn:10006/assets/default_bg.jpg')
    desc = Column(Text)
    vip = Column(Integer, default=0)
    token = Column(String(255))
    token_expire = Column(DATETIME)
    createdAt = Column(DATETIME, nullable=False, default=datetime.now)
    updatedAt = Column(DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now)

class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String(20), unique=True, nullable=False)
    typeDesc = Column(String(20), nullable=False)
    createdAt = Column(DATETIME, nullable=False, default=datetime.now)
    updatedAt = Column(DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    products = relationship("Product", back_populates="product_type")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pid = Column(String(20), unique=True, nullable=False)
    type = Column(String(20), ForeignKey("product_types.type"), nullable=False)
    name = Column(String(100), nullable=False)
    enname = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    desc = Column(Text, nullable=False)
    smallImg = Column(String(255), nullable=False)
    largeImg = Column(String(255), nullable=False)
    isHot = Column(Integer, default=0)
    tem = Column(String(50))
    tem_desc = Column(String(50))
    sugar = Column(String(50))
    sugar_desc = Column(String(50))
    milk = Column(String(50))
    milk_desc = Column(String(50))
    cream = Column(String(50))
    cream_desc = Column(String(50))
    createdAt = Column(DATETIME, nullable=False, default=datetime.now)
    updatedAt = Column(DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 关联关系
    product_type = relationship("ProductType", back_populates="products")
    # specs = relationship("ProductSpec", back_populates="product")

class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    imgUrl = Column(String(255), nullable=False)
    desc = Column(String(255), nullable=False)
    sort_order = Column(Integer, default=0)
    createdAt = Column(DATETIME, nullable=False, default=datetime.now)
    updatedAt = Column(DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now)

# class ProductSpec(Base):
#     __tablename__ = "product_specs"

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     pid = Column(String(20), ForeignKey("products.pid"), nullable=False)
#     spec_type = Column(Enum('tem', 'sugar', 'milk', 'cream'), nullable=False)
#     spec_value = Column(String(50), nullable=False)
#     spec_desc = Column(String(50))

#     # 关联关系
#     product = relationship("Product", back_populates="specs")