from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    DB_HOST: str = "mysql"
    DB_PORT: int = 3306
    DB_USER: str = "Jerry"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "COM6102"
    
    # Redis配置
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200

    # 环境配置
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'

settings = Settings()

# 数据库URL - 添加连接参数确保可靠性
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8mb4&connect_timeout=20"

# Redis URL
REDIS_URL = f"redis://{':' + settings.REDIS_PASSWORD + '@' if settings.REDIS_PASSWORD else ''}{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"