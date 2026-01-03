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

def add_monitor_record(session, 物种编号, 监测设备编号, 监测时间, 经度, 纬度,
                       监测方式, 监测内容, 记录人ID, 数据状态, 分析结论=None):
    try:
        new_record = 监测记录(
            物种编号=物种编号,
            监测设备编号=监测设备编号,
            监测时间=监测时间,
            经度=经度,
            纬度=纬度,
            监测方式=监测方式,
            监测内容=监测内容,
            记录人ID=记录人ID,
            数据状态=数据状态,
            分析结论=分析结论
        )
        session.add(new_record)
        session.flush()  # 立即生成记录编号
        return new_record.记录编号
    except SQLAlchemyError as e:
        session.rollback()
        print(f"添加监测记录失败: {e}")
        return None

def delete_monitor_record(session, 记录编号):
    try:
        stmt = delete(监测记录).where(监测记录.记录编号 == 记录编号)
        result = session.execute(stmt)
        return result.rowcount  # 返回删除的行数
    except SQLAlchemyError as e:
        session.rollback()
        print(f"删除监测记录失败: {e}")
        return 0

def update_monitor_record(session, 记录编号, 数据状态=None, 分析结论=None):
    try:
        stmt = update(监测记录).where(监测记录.记录编号 == 记录编号)
        update_values = {}
        if 数据状态 is not None:
            update_values['数据状态'] = 数据状态
        if 分析结论 is not None:
            update_values['分析结论'] = 分析结论
        if not update_values:
            return 0  # 没有需要更新的值
        stmt = stmt.values(**update_values)
        result = session.execute(stmt)
        return result.rowcount  # 返回更新的行数
    except SQLAlchemyError as e:
        session.rollback()
        print(f"更新监测记录失败: {e}")
        return 0

def query_monitor_records(session, 记录编号=None, 物种编号=None, 数据状态=None):
    try:
        stmt = select(监测记录)
        if 记录编号 is not None:
            stmt = stmt.where(监测记录.记录编号 == 记录编号)
        if 物种编号 is not None:
            stmt = stmt.where(监测记录.物种编号 == 物种编号)
        if 数据状态 is not None:
            stmt = stmt.where(监测记录.数据状态 == 数据状态)
        result = session.execute(stmt).scalars().all()
        return result
    except SQLAlchemyError as e:
        print(f"查询监测记录失败: {e}")
        return []

