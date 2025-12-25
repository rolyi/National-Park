from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from datetime import datetime
DATABASE_CONFIG = {
    "driver": "mysql+pymysql",
    "user": "yi",
    "password": "2224965152",
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

Base = declarative_base()

class 物种信息(Base):
    __tablename__ = "物种信息"

    物种编号 = Column(Integer, primary_key=True)
    中文名称 = Column(String(50), nullable=False)
    拉丁名 = Column(String(50), nullable=False)
    物种分类 = Column(Text, nullable=False)
    保护级别 = Column(String(10), nullable=False)
    生存习性 = Column(Text, nullable=False)
    分布范围 = Column(Text, nullable=False)

class 监测记录(Base):
    __tablename__ = "监测记录"

    记录编号 = Column(Integer, primary_key=True)
    物种编号 = Column(Integer, ForeignKey("物种信息.物种编号"), nullable=False)
    监测设备编号 = Column(Integer, nullable=False)
    监测时间 = Column(DateTime, nullable=False)
    经度 = Column(Numeric(9, 6), nullable=False)
    纬度 = Column(Numeric(9, 6), nullable=False)
    监测方式 = Column(String(10), nullable=False)
    监测内容 = Column(Text, nullable=False)
    记录人ID = Column(Integer, nullable=False)
    数据状态 = Column(String(10), nullable=False)
    分析结论 = Column(Text)

class 栖息地信息(Base):
    __tablename__ = "栖息地信息"

    栖息地编号 = Column(Integer, primary_key=True)
    区域名称 = Column(String(50), nullable=False)
    生态类型 = Column(String(20), nullable=False)
    面积 = Column(Numeric(5, 1), nullable=False)
    核心保护范围 = Column(Text, nullable=False)


class 物种栖息关系(Base):
    __tablename__ = "物种信息_栖息地信息_栖息"

    物种编号 = Column(Integer, ForeignKey("物种信息.物种编号"), primary_key=True)
    栖息地编号 = Column(Integer, ForeignKey("栖息地信息.栖息地编号"), primary_key=True)
    环境适应性评分 = Column(Integer, nullable=False)

def query_物种信息():
    with get_db_session() as session:
        数据列表 = session.query(物种信息).all()
        for 行 in 数据列表:
            print(
                f"物种编号：{行.物种编号}, "
                f"中文名称：{行.中文名称}, "
                f"拉丁名：{行.拉丁名}, "
                f"物种分类：{行.物种分类}, "
                f"保护级别：{行.保护级别}, "
                f"生存习性：{行.生存习性}, "
                f"分布范围：{行.分布范围}"
            )

def query_监测记录():
    with get_db_session() as session:
        数据列表 = session.query(监测记录).all()
        for 行 in 数据列表:
            print(
                f"记录编号：{行.记录编号}, "
                f"物种编号：{行.物种编号}, "
                f"监测设备编号：{行.监测设备编号}, "
                f"监测时间：{行.监测时间}, "
                f"经度：{行.经度}, "
                f"纬度：{行.纬度}, "
                f"监测方式：{行.监测方式}, "
                f"监测内容：{行.监测内容}, "
                f"记录人ID：{行.记录人ID}, "
                f"数据状态：{行.数据状态}, "
                f"分析结论：{行.分析结论}"
            )

def query_栖息地信息():
    with get_db_session() as session:
        数据列表 = session.query(栖息地信息).all()
        for 行 in 数据列表:
            print(
                f"栖息地编号：{行.栖息地编号}, "
                f"区域名称：{行.区域名称}, "
                f"生态类型：{行.生态类型}, "
                f"面积：{行.面积}, "
                f"核心保护范围：{行.核心保护范围}"
            )

def query_物种栖息关系():
    with get_db_session() as session:
        数据列表 = session.query(物种栖息关系).all()
        for 行 in 数据列表:
            print(
                f"物种编号：{行.物种编号}, "
                f"栖息地编号：{行.栖息地编号}, "
                f"环境适应性评分：{行.环境适应性评分}"
            )

if __name__ == "__main__":
    query_物种信息()
    query_监测记录()
    query_栖息地信息()
    query_物种栖息关系()
