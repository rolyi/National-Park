from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
DATABASE_CONFIG = {
    "driver": "mysql+pymysql",
    "user": "user",
    "password": "the_password",
    "host": "81.70.99.15",
    "port": 3306,
    "db_name": "国家公园",
    "charset": "utf8"
}
DATABASE_URL = f"{DATABASE_CONFIG['driver']}://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@" \
               f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['db_name']}?charset=utf8mb4"
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # 默认连接数
    max_overflow=20,  # 最大临时连接数（超过pool_size时）
    pool_recycle=3600,  # 连接超时时间（秒），避免数据库主动断开连接
    echo=False  # 生产环境关闭SQL日志输出
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()  # 无异常时自动提交
    except Exception as e:
        session.rollback()  # 异常时自动回滚
        raise e  # 抛出异常便于上层处理
    finally:
        session.close()  # 无论成败都关闭会话

