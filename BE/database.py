from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from config import DATABASE_URL

# 创建数据库引擎，简化配置
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # 基本连接池大小
    max_overflow=10,  # 最大溢出连接数
    pool_recycle=3600,  # 1小时回收连接
    pool_pre_ping=True,  # 执行前ping测试连接
    connect_args={
        'connect_timeout': 10  # 连接超时时间
    },
    isolation_level="READ COMMITTED"
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本模型类
Base = declarative_base()

# 连接池预热
def warm_up_pool():
    """预热连接池，创建初始连接"""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db.close()
    except Exception as e:
        db.close()
        raise e

# 监听连接池创建事件
@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    """设置连接的wait_timeout"""
    cursor = dbapi_connection.cursor()
    try:
        # 直接使用字符串，因为这是PyMySQL的cursor
        cursor.execute("SET SESSION wait_timeout=28800")  # 8小时
        cursor.execute("SET SESSION interactive_timeout=28800")  # 8小时
    finally:
        cursor.close()

# 获取数据库会话的依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化时预热连接池
try:
    warm_up_pool()
except Exception as e:
    print(f"Warning: Failed to warm up connection pool: {e}")

