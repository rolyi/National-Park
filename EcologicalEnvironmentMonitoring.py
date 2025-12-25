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

class 监测指标信息(Base):
    __tablename__ = "监测指标信息"

    指标编号 = Column(Integer, primary_key=True)
    指标名称 = Column(String(20), nullable=False)
    计量单位 = Column(String(20), nullable=False)
    阈值上限 = Column(Numeric(5, 1), nullable=False)
    阈值下限 = Column(Numeric(5, 1), nullable=False)
    监测频率 = Column(String(10))

class 环境监测数据(Base):
    __tablename__ = "环境监测数据"

    数据编号 = Column(Integer, primary_key=True)
    采集时间 = Column(DateTime, nullable=False)
    数据质量 = Column(String(10), nullable=False)

class 监测设备信息(Base):
    __tablename__ = "监测设备信息"

    设备编号 = Column(Integer, primary_key=True)
    设备类型 = Column(String(20), nullable=False)
    安装时间 = Column(DateTime, nullable=False)
    校准周期 = Column(String(10), nullable=False)
    校准记录 = Column(Text, nullable=False)
    通信协议 = Column(String(20), nullable=False)
    运行状态 = Column(String(10), nullable=False)

class 监测指标_数据关联(Base):
    __tablename__ = "监测指标信息_环境监测数据_关联"

    指标编号 = Column(Integer, ForeignKey("监测指标信息.指标编号"), primary_key=True)
    数据编号 = Column(Integer, ForeignKey("环境监测数据.数据编号"), primary_key=True)

class 数据_设备监测(Base):
    __tablename__ = "环境监测数据_监测设备信息_监测"

    数据编号 = Column(Integer, ForeignKey("环境监测数据.数据编号"), primary_key=True)
    设备编号 = Column(Integer, ForeignKey("监测设备信息.设备编号"), primary_key=True)
    监测值 = Column(Numeric(5,1), nullable=False)
    区域编号 = Column(Integer, nullable=False)
    功能分区 = Column(String(20), nullable=False)

def query_监测指标信息():
    with get_db_session() as session:
        列表 = session.query(监测指标信息).all()
        for 行 in 列表:
            print(f"指标编号：{行.指标编号}, 指标名称：{行.指标名称}, 计量单位：{行.计量单位}, "
                  f"阈值上限：{行.阈值上限}, 阈值下限：{行.阈值下限}, 监测频率：{行.监测频率}")

def query_环境监测数据():
    with get_db_session() as session:
        列表 = session.query(环境监测数据).all()
        for 行 in 列表:
            print(f"数据编号：{行.数据编号}, 采集时间：{行.采集时间}, 数据质量：{行.数据质量}")

def query_监测设备信息():
    with get_db_session() as session:
        列表 = session.query(监测设备信息).all()
        for 行 in 列表:
            print(f"设备编号：{行.设备编号}, 设备类型：{行.设备类型}, 安装时间：{行.安装时间}, "
                  f"校准周期：{行.校准周期}, 校准记录：{行.校准记录}, 通信协议：{行.通信协议}, "
                  f"运行状态：{行.运行状态}")

def query_监测指标_数据关联():
    with get_db_session() as session:
        列表 = session.query(监测指标_数据关联).all()
        for 行 in 列表:
            print(f"指标编号：{行.指标编号}, 数据编号：{行.数据编号}")

def query_数据_设备监测():
    with get_db_session() as session:
        列表 = session.query(数据_设备监测).all()
        for 行 in 列表:
            print(f"数据编号：{行.数据编号}, 设备编号：{行.设备编号}, 监测值：{行.监测值}, "
                  f"区域编号：{行.区域编号}, 功能分区：{行.功能分区}")

if __name__ == "__main__":
    query_环境监测数据()
    query_监测指标信息()
    query_监测设备信息()
    query_数据_设备监测()
    query_监测指标_数据关联()
