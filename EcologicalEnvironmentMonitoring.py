from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

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

def update_monitor_threshold(session, 指标编号, 阈值上限=None, 阈值下限=None):
    try:
        stmt = update(监测指标信息).where(监测指标信息.指标编号 == 指标编号)
        update_values = {}
        if 阈值上限 is not None:
            update_values['阈值上限'] = 阈值上限
        if 阈值下限 is not None:
            update_values['阈值下限'] = 阈值下限
        if not update_values:
            return 0
        stmt = stmt.values(**update_values)
        result = session.execute(stmt)
        return result.rowcount
    except SQLAlchemyError as e:
        session.rollback()
        print(f"更新监测指标阈值失败: {e}")
        return 0


def update_device_status(session, 设备编号, 运行状态=None, 校准记录=None):
    try:
        stmt = update(监测设备信息).where(监测设备信息.设备编号 == 设备编号)
        update_values = {}
        if 运行状态 is not None:
            update_values['运行状态'] = 运行状态
        if 校准记录 is not None:
            update_values['校准记录'] = 校准记录
        if not update_values:
            return 0
        stmt = stmt.values(**update_values)
        result = session.execute(stmt)
        return result.rowcount
    except SQLAlchemyError as e:
        session.rollback()
        print(f"更新设备信息失败: {e}")
        return 0


def add_environment_data(session, 采集时间, 数据质量):
    try:
        new_data = 环境监测数据(
            采集时间=采集时间,
            数据质量=数据质量
        )
        session.add(new_data)
        session.flush()  # 生成数据编号
        return new_data.数据编号
    except SQLAlchemyError as e:
        session.rollback()
        print(f"添加环境监测数据失败: {e}")
        return None


def add_data_device_monitor(session, 数据编号, 设备编号, 监测值, 区域编号, 功能分区):
    try:
        new_record = 数据_设备监测(
            数据编号=数据编号,
            设备编号=设备编号,
            监测值=监测值,
            区域编号=区域编号,
            功能分区=功能分区
        )
        session.add(new_record)
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"添加数据_设备监测失败: {e}")
        return False


def delete_environment_data(session, 数据编号):
    try:
        # 先删除关联表
        session.execute(delete(监测指标_数据关联).where(监测指标_数据关联.数据编号 == 数据编号))
        session.execute(delete(数据_设备监测).where(数据_设备监测.数据编号 == 数据编号))
        result = session.execute(delete(环境监测数据).where(环境监测数据.数据编号 == 数据编号))
        return result.rowcount
    except SQLAlchemyError as e:
        session.rollback()
        print(f"删除环境监测数据失败: {e}")
        return 0

def query_environment_data_by_id(session, 数据编号):
    try:
        stmt = select(环境监测数据).where(环境监测数据.数据编号 == 数据编号)
        result = session.execute(stmt).scalars().all()
        return result
    except SQLAlchemyError as e:
        print(f"查询环境监测数据失败: {e}")
        return []

def query_environment_data_by_indicator(session, 指标编号):
    try:
        stmt = (
            select(环境监测数据)
            .join(监测指标_数据关联, 环境监测数据.数据编号 == 监测指标_数据关联.数据编号)
            .where(监测指标_数据关联.指标编号 == 指标编号)
        )
        result = session.execute(stmt).scalars().all()
        return result
    except SQLAlchemyError as e:
        print(f"按指标编号查询环境监测数据失败: {e}")
        return []
