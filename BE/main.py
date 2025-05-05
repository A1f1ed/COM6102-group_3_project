
import sys
import platform

# 检查Python版本
if sys.version_info < (3, 10):
    sys.exit("Python 3.10 or above is required.")

from fastapi import FastAPI, Depends
from redis_utils import RedisUtils
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from database import engine, Base, SessionLocal
from routers import auth, users, products, promotions
from starlette_prometheus import PrometheusMiddleware, metrics

# 创建FastAPI应用实例
app = FastAPI(
    title="Coffee Shop API",
    description="咖啡店后端API服务",
    version="1.0.0",
    openapi_tags=[
        {"name": "认证", "description": "用户认证相关接口"},
        {"name": "用户", "description": "用户信息相关接口"},
        {"name": "商品", "description": "商品相关接口"},
        {"name": "推广", "description": "推广内容相关接口"},
    ]
)

# 添加启动事件处理程序
from sqlalchemy import text
import time

@app.get("/health")
async def health_check():
    """健康检查接口"""
    db = SessionLocal()
    try:
        # 测试数据库连接
        db.execute(text("SELECT 1"))
        # 测试Redis连接
        if RedisUtils.redis_client is None:
            raise Exception("Redis client not initialized")
        await RedisUtils.redis_client.ping()
        return {"status": "healthy", "database": "connected", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化连接"""
    # 初始化数据库连接（带重试）
    max_retries = 5
    retry_delay = 5
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            # 测试数据库连接
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            print(f"✅ Database connection successful (attempt {attempt + 1})")
            db.close()
            break
        except Exception as e:
            last_exception = e
            print(f"❌ Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached, unable to connect to database")
                raise last_exception

    # 初始化Redis连接
    await RedisUtils.init_redis(app)
    print("✅ Redis connection initialized")

# 添加关闭事件处理程序
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理Redis连接"""
    await RedisUtils.close_redis()

# 添加Prometheus监控
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由 - 确保auth路由先注册
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(promotions.router)

@app.get("/")
async def root():
    return {"message": "欢迎使用咖啡店API服务"}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)