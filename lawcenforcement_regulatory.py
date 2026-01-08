from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Numeric, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from datetime import datetime, timedelta

# ------------------------------ 基础配置（保留原有配置） ------------------------------
LOGIN_FAIL_COUNT = {}
LOCK_UNTIL = {}
LAST_ACTIVE_TIME = {}

MAX_FAIL_TIMES = 5
LOCK_DURATION = timedelta(minutes=1)
SESSION_TIMEOUT = timedelta(minutes=30)

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
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


Base = declarative_base()


# ------------------------------ 原有基础权限表（保留） ------------------------------
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(100), nullable=False)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    resource = Column(String(50))


class user_roles(Base):
    __tablename__ = "user_roles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)


class role_permissions(Base):
    __tablename__ = "role_permissions"
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)


# ------------------------------ 原有生态环境监测业务线模型（保留） ------------------------------
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
    监测值 = Column(Numeric(5, 1), nullable=False)
    区域编号 = Column(Integer, nullable=False)
    功能分区 = Column(String(20), nullable=False)


class 技术人员_设备维护(Base):
    __tablename__ = "技术人员_设备维护"
    设备编号 = Column(Integer, primary_key=True)
    设备类型 = Column(String(20))
    安装时间 = Column(DateTime)
    校准周期 = Column(String(10))
    校准记录 = Column(Text)
    通信协议 = Column(String(20))
    运行状态 = Column(String(10))
    区域编号 = Column(Integer)
    功能分区 = Column(String(20))


class 数据分析师_生态环境监测_分析(Base):
    __tablename__ = "数据分析师_生态环境监测_分析"
    数据编号 = Column(Integer, primary_key=True)
    指标名称 = Column(String(20))
    计量单位 = Column(String(20))
    阈值上限 = Column(Numeric(5, 1))
    阈值下限 = Column(Numeric(5, 1))
    采集时间 = Column(DateTime)
    数据质量 = Column(String(10))
    监测值 = Column(Numeric(5, 1))
    区域编号 = Column(Integer)
    功能分区 = Column(String(20))


class 数据分析师_生态环境监测_阈值维护(Base):
    __tablename__ = "数据分析师_生态环境监测_阈值维护"
    指标名称 = Column(String(20), primary_key=True)
    计量单位 = Column(String(20))
    阈值上限 = Column(Numeric(5, 1))
    阈值下限 = Column(Numeric(5, 1))


# ------------------------------ 新增：执法监管业务线核心ORM模型（严格按指定表结构） ------------------------------
class 执法人员信息(Base):
    __tablename__ = "执法人员信息"
    # 指定字段：执法ID、调度编号、记录编号、姓名、部门、权限、联系方式、执法设备编号
    执法ID = Column(Integer, primary_key=True)
    调度编号 = Column(Integer, ForeignKey("执法调度信息.调度编号"), nullable=True)
    记录编号 = Column(Integer, ForeignKey("非法行为记录.记录编号"), nullable=True)
    姓名 = Column(String(50), nullable=False)
    部门 = Column(String(50), nullable=False)
    权限 = Column(String(100), nullable=False)
    联系方式 = Column(String(20), nullable=False)
    执法设备编号 = Column(Integer, nullable=False)


class 非法行为记录(Base):
    __tablename__ = "非法行为记录"
    # 指定字段：记录编号、行为类型、发生时间、发生区域编号、影像证据路径、处理状态、执法ID、处理结果、处罚依据
    记录编号 = Column(Integer, primary_key=True)
    行为类型 = Column(String(30), nullable=False)
    发生时间 = Column(DateTime, nullable=False)
    发生区域编号 = Column(Integer, nullable=False)
    影像证据路径 = Column(Text, nullable=False)
    处理状态 = Column(String(10), nullable=False)
    执法ID = Column(Integer, ForeignKey("执法人员信息.执法ID"), nullable=False)
    处理结果 = Column(Text)
    处罚依据 = Column(String(100), nullable=False)


class 执法调度信息(Base):
    __tablename__ = "执法调度信息"
    # 指定字段：调度编号、调度时间、响应时间、处置完成时间、调度状态
    调度编号 = Column(Integer, primary_key=True)
    调度时间 = Column(DateTime, nullable=False)
    响应时间 = Column(DateTime)
    处置完成时间 = Column(DateTime)
    调度状态 = Column(String(10), nullable=False)


class 视频监控点信息(Base):
    __tablename__ = "视频监控点信息"
    # 指定字段：监控点编号、区域编号、经度、纬度、设备状态、监控范围、数据存储周期
    监控点编号 = Column(Integer, primary_key=True)
    区域编号 = Column(Integer, nullable=False)
    经度 = Column(Numeric(9, 6), nullable=False)
    纬度 = Column(Numeric(9, 6), nullable=False)
    设备状态 = Column(String(10), nullable=False)
    监控范围 = Column(String(50), nullable=False)
    数据存储周期 = Column(Integer, nullable=False)


# ------------------------------ 新增：执法监管业务线视图模型（严格按指定表结构） ------------------------------
class 执法人员_个人执法统计(Base):
    __tablename__ = "执法人员_个人执法统计"
    __table_args__ = {'extend_existing': True}
    # 指定字段：执法ID、姓名、所属部门、总处理任务数、已完成任务数、平均响应时长分钟、平均处置时长小时、主要处理行为类型
    执法ID = Column(Integer, primary_key=True)
    姓名 = Column(String(50))
    所属部门 = Column(String(50))
    总处理任务数 = Column(Integer)
    已完成任务数 = Column(Integer)
    平均响应时长分钟 = Column(Integer)
    平均处置时长小时 = Column(Numeric(5, 1))
    主要处理行为类型 = Column(String(50))


class 执法人员_个人统计视图(Base):
    __tablename__ = "执法人员_个人统计视图"
    __table_args__ = {'extend_existing': True}
    # 指定字段：执法ID、姓名、处理案件总数、已结案数、平均处置时长、未响应调度数
    执法ID = Column(Integer, primary_key=True)
    姓名 = Column(String(50))
    处理案件总数 = Column(Integer)
    已结案数 = Column(Integer)
    平均处置时长 = Column(Numeric(5, 1))
    未响应调度数 = Column(Integer)


class 执法人员_非法行为处理视图(Base):
    __tablename__ = "执法人员_非法行为处理视图"
    __table_args__ = {'extend_existing': True}
    # 指定字段：调度编号、非法行为记录编号、行为类型、发生时间、发生区域编号、影像证据路径、处理状态、调度状态、调度时间
    调度编号 = Column(Integer, primary_key=True)
    非法行为记录编号 = Column(Integer)
    行为类型 = Column(String(30))
    发生时间 = Column(DateTime)
    发生区域编号 = Column(Integer)
    影像证据路径 = Column(Text)
    处理状态 = Column(String(10))
    调度状态 = Column(String(10))
    调度时间 = Column(DateTime)


# ------------------------------ 新增：执法监管视图创建SQL（确保与ORM模型一致） ------------------------------
def create_law_enforcement_views():
    """创建执法监管业务线3个核心视图"""
    with get_db_session() as session:
        # 1. 执法人员_个人执法统计视图
        session.execute(text("""
        CREATE OR REPLACE VIEW 执法人员_个人执法统计 AS
        SELECT
            e.执法ID,
            e.姓名,
            e.部门 AS 所属部门,
            COUNT(d.调度编号) AS 总处理任务数,
            SUM(CASE WHEN d.调度状态 = '已完成' THEN 1 ELSE 0 END) AS 已完成任务数,
            ROUND(AVG(IF(d.响应时间 IS NOT NULL, TIMESTAMPDIFF(MINUTE, d.调度时间, d.响应时间), 0))) AS 平均响应时长分钟,
            ROUND(AVG(IF(d.处置完成时间 IS NOT NULL AND d.响应时间 IS NOT NULL, 
                        TIMESTAMPDIFF(MINUTE, d.响应时间, d.处置完成时间)/60, 0)), 1) AS 平均处置时长小时,
            (SELECT r.行为类型 
             FROM 非法行为记录 r
             WHERE r.执法ID = e.执法ID
             GROUP BY r.行为类型
             ORDER BY COUNT(*) DESC
             LIMIT 1) AS 主要处理行为类型
        FROM 执法人员信息 e
        LEFT JOIN 执法调度信息 d ON e.调度编号 = d.调度编号
        GROUP BY e.执法ID, e.姓名, e.部门;
        """))

        # 2. 执法人员_个人统计视图
        session.execute(text("""
        CREATE OR REPLACE VIEW 执法人员_个人统计视图 AS
        SELECT
            e.执法ID,
            e.姓名,
            COUNT(r.记录编号) AS 处理案件总数,
            SUM(CASE WHEN r.处理状态 = '已结案' THEN 1 ELSE 0 END) AS 已结案数,
            ROUND(AVG(IF(d.处置完成时间 IS NOT NULL, 
                        TIMESTAMPDIFF(MINUTE, d.调度时间, d.处置完成时间)/60, 0)), 1) AS 平均处置时长,
            SUM(CASE WHEN d.调度状态 = '待响应' AND TIMESTAMPDIFF(MINUTE, d.调度时间, NOW()) > 30 
                     THEN 1 ELSE 0 END) AS 未响应调度数
        FROM 执法人员信息 e
        LEFT JOIN 非法行为记录 r ON e.记录编号 = r.记录编号
        LEFT JOIN 执法调度信息 d ON e.调度编号 = d.调度编号
        GROUP BY e.执法ID, e.姓名;
        """))

        # 3. 执法人员_非法行为处理视图
        session.execute(text("""
        CREATE OR REPLACE VIEW 执法人员_非法行为处理视图 AS
        SELECT
            d.调度编号,
            r.记录编号 AS 非法行为记录编号,
            r.行为类型,
            r.发生时间,
            r.发生区域编号,
            r.影像证据路径,
            r.处理状态,
            d.调度状态,
            d.调度时间
        FROM 执法调度信息 d
        LEFT JOIN 执法人员信息 e ON d.调度编号 = e.调度编号
        LEFT JOIN 非法行为记录 r ON e.记录编号 = r.记录编号
        WHERE r.记录编号 IS NOT NULL;
        """))

        session.commit()
        print("执法监管业务线视图创建成功！")


# ------------------------------ 新增：执法人员核心业务逻辑 ------------------------------
def 执法人员_接收调度(执法ID: int, 调度编号: int) -> str:
    """执法人员接收调度任务"""
    with get_db_session() as session:
        调度记录 = session.query(执法调度信息).filter_by(调度编号=调度编号).first()
        if not 调度记录:
            return f"错误：调度编号{调度编号}不存在"
        if 调度记录.调度状态 != "待响应":
            return f"错误：调度状态已为【{调度记录.调度状态}】"

        执法人员 = session.query(执法人员信息).filter_by(执法ID=执法ID, 调度编号=调度编号).first()
        if not 执法人员:
            return "错误：您无权限接收该调度"

        调度记录.响应时间 = datetime.now()
        调度记录.调度状态 = "已派单"
        session.commit()
        return f"成功接收调度！响应时间：{调度记录.响应时间.strftime('%Y-%m-%d %H:%M:%S')}"


def 执法人员_提交处置结果(执法ID: int, 调度编号: int, 处理结果: str, 处理状态: str = "已结案") -> str:
    """提交非法行为处置结果"""
    with get_db_session() as session:
        调度记录 = session.query(执法调度信息).filter_by(调度编号=调度编号).first()
        if not 调度记录:
            return f"错误：调度编号{调度编号}不存在"
        if 调度记录.调度状态 != "已派单":
            return f"错误：调度状态为【{调度记录.调度状态}】"

        执法人员 = session.query(执法人员信息).filter_by(执法ID=执法ID, 调度编号=调度编号).first()
        if not 执法人员:
            return "错误：您无权限处理该调度"

        非法行为记录_obj = session.query(非法行为记录).filter_by(记录编号=执法人员.记录编号).first()
        if not 非法行为记录_obj:
            return "错误：未找到关联的非法行为记录"

        调度记录.处置完成时间 = datetime.now()
        调度记录.调度状态 = "已完成"
        非法行为记录_obj.处理状态 = 处理状态
        非法行为记录_obj.处理结果 = 处理结果
        session.commit()
        return f"处置结果提交成功！案件状态：{处理状态}"


def 执法人员_查询个人统计(执法ID: int) -> dict | str:
    """查询个人执法统计数据"""
    with get_db_session() as session:
        统计数据 = session.query(执法人员_个人执法统计).filter_by(执法ID=执法ID).first()
        if not 统计数据:
            return "暂无统计数据"
        return {
            "执法ID": 统计数据.执法ID,
            "姓名": 统计数据.姓名,
            "所属部门": 统计数据.所属部门,
            "总处理任务数": 统计数据.总处理任务数 or 0,
            "已完成任务数": 统计数据.已完成任务数 or 0,
            "平均响应时长(分钟)": 统计数据.平均响应时长分钟 or 0,
            "平均处置时长(小时)": float(统计数据.平均处置时长小时) if 统计数据.平均处置时长小时 else 0.0,
            "主要处理行为类型": 统计数据.主要处理行为类型 or "无"
        }


# ------------------------------ 更新：表映射与只读视图配置 ------------------------------
TABLE_MAP = {
    # 原有表映射
    "监测指标信息": 监测指标信息,
    "环境监测数据": 环境监测数据,
    "监测设备信息": 监测设备信息,
    "监测指标_数据关联": 监测指标_数据关联,
    "数据_设备监测": 数据_设备监测,
    "环境监测数据－监测设备信息－监测": 数据_设备监测,
    "监测指标信息－环境监测数据－关联": 监测指标_数据关联,
    "数据分析师_生态环境监测_阈值维护": 数据分析师_生态环境监测_阈值维护,
    "数据分析师_生态环境监测_分析": 数据分析师_生态环境监测_分析,
    "技术人员_设备维护": 技术人员_设备维护,
    # 新增执法监管表映射
    "执法人员信息": 执法人员信息,
    "非法行为记录": 非法行为记录,
    "执法调度信息": 执法调度信息,
    "视频监控点信息": 视频监控点信息,
    "执法人员_个人执法统计": 执法人员_个人执法统计,
    "执法人员_个人统计视图": 执法人员_个人统计视图,
    "执法人员_非法行为处理视图": 执法人员_非法行为处理视图
}

READ_ONLY_VIEWS = {
    # 原有只读视图
    "数据分析师_生态环境监测_阈值维护": 数据分析师_生态环境监测_阈值维护,
    "数据分析师_生态环境监测_分析": 数据分析师_生态环境监测_分析,
    "技术人员_设备维护": 技术人员_设备维护,
    # 新增执法监管只读视图
    "执法人员_个人执法统计": 执法人员_个人执法统计,
    "执法人员_个人统计视图": 执法人员_个人统计视图,
    "执法人员_非法行为处理视图": 执法人员_非法行为处理视图
}


# ------------------------------ 更新：登录逻辑（绑定执法ID） ------------------------------
def login(username: str, password: str):
    now = datetime.now()

    if username in LOCK_UNTIL:
        if now < LOCK_UNTIL[username]:
            remain = int((LOCK_UNTIL[username] - now).total_seconds())
            print(f"账户已锁定，请 {remain} 秒后再试")
            return None
        else:
            LOCK_UNTIL.pop(username)
            LOGIN_FAIL_COUNT[username] = 0

    with get_db_session() as session:
        user = session.query(User).filter(
            User.username == username,
            User.password == password
        ).first()

        if not user:
            LOGIN_FAIL_COUNT[username] = LOGIN_FAIL_COUNT.get(username, 0) + 1
            if LOGIN_FAIL_COUNT[username] >= MAX_FAIL_TIMES:
                LOCK_UNTIL[username] = now + LOCK_DURATION
                print("连续 5 次失败，账户已锁定 1 分钟")
            else:
                left = MAX_FAIL_TIMES - LOGIN_FAIL_COUNT[username]
                print(f"用户名或密码错误，还可尝试 {left} 次")
            return None

        LOGIN_FAIL_COUNT[username] = 0
        LAST_ACTIVE_TIME[username] = now

        roles = (
            session.query(Role)
            .join(user_roles, Role.id == user_roles.role_id)
            .filter(user_roles.user_id == user.id)
            .all()
        )

        role_ids = [r.id for r in roles]

        permissions = []
        if role_ids:
            permissions = (
                session.query(Permission.resource)
                .join(role_permissions, Permission.id == role_permissions.permission_id)
                .filter(role_permissions.role_id.in_(role_ids))
                .distinct()
                .all()
            )

        login_result = {
            "user_id": user.id,
            "username": user.username,
            "roles": [r.role_name for r in roles],
            "permissions": [p.resource for p in permissions],
            "login_time": now
        }

        # 绑定执法ID（针对执法人员角色）
        if "执法人员" in login_result["roles"]:
            执法人员 = session.query(执法人员信息).filter_by(姓名=username).first()
            if 执法人员:
                login_result["执法ID"] = 执法人员.执法ID

        return login_result


# ------------------------------ 更新：主菜单（添加执法人员专属操作） ------------------------------
def 执法人员专属操作(user, session):
    """执法人员专属功能菜单"""
    print("\n===== 执法人员专属操作 =====")
    print("1. 查看个人执法统计（详细版）")
    print("2. 查看个人统计（简化版）")
    print("3. 查看非法行为处理记录")
    print("4. 接收调度任务")
    print("5. 提交处置结果")
    print("6. 返回主菜单")
    choice = input("请选择：")

    执法ID = user.get("执法ID")
    if not 执法ID and choice != "6":
        print("错误：未获取到执法ID")
        return

    if choice == "1":
        统计数据 = 执法人员_查询个人统计(执法ID)
        if isinstance(统计数据, dict):
            print("\n===== 个人执法统计 =====")
            for k, v in 统计数据.items():
                print(f"{k}：{v}")
        else:
            print(统计数据)
    elif choice == "2":
        print_table(user, session)  # 直接调用原有查看表功能
    elif choice == "3":
        print_table(user, session)
    elif choice == "4":
        调度编号 = input("请输入要接收的调度编号：")
        try:
            调度编号 = int(调度编号)
            结果 = 执法人员_接收调度(执法ID, 调度编号)
            print(结果)
        except ValueError:
            print("错误：调度编号必须为数字")
    elif choice == "5":
        调度编号 = input("请输入调度编号：")
        处理结果 = input("请输入处置结果：")
        try:
            调度编号 = int(调度编号)
            结果 = 执法人员_提交处置结果(执法ID, 调度编号, 处理结果)
            print(结果)
        except ValueError:
            print("错误：调度编号必须为数字")


def choose():
    username = input("username: ")
    password = input("password: ")

    user = login(username, password)
    if not user:
        return

    print(f"欢迎您 {'、'.join(user['roles'])}")

    while True:
        if not check_session(username):
            break

        print("\n1. 查看表")
        print("2. 插入数据")
        print("3. 删除数据")
        print("4. 更新数据")
        print("5. 查询数据")
        if "执法人员" in user["roles"]:
            print("6. 执法人员专属操作")
        print("0. 退出账户")
        choice = input("请选择：")

        with get_db_session() as session:
            if choice == "0":
                print("已退出")
                break
            elif choice == "1":
                print_table(user, session)
            elif choice == "2":
                insert_row(user, session)
            elif choice == "3":
                delete_row(user, session)
            elif choice == "4":
                update_row(user, session)
            elif choice == "5":
                query_row(user, session)
            elif choice == "6" and "执法人员" in user["roles"]:
                执法人员专属操作(user, session)
            else:
                print("选择无效")


# ------------------------------ 更新：主函数（初始化执法监管视图） ------------------------------
def run():
    # 首次运行创建执法监管视图
    try:
        create_law_enforcement_views()
    except Exception as e:
        print(f"视图创建提示：{str(e)[:200]}（若已创建可忽略）")

    while True:
        print("1.登录")
        print("2.退出系统")
        choice = input("请选择：")
        if choice == "1":
            choose()
        elif choice == "2":
            break
        else:
            print("选择无效")


# ------------------------------ 原有工具函数（print_table/insert_row等）保留不变 ------------------------------
def check_session(username: str):
    now = datetime.now()
    last_time = LAST_ACTIVE_TIME.get(username)
    if not last_time:
        print("未登录或会话已失效")
        return False
    if now - last_time > SESSION_TIMEOUT:
        LAST_ACTIVE_TIME.pop(username, None)
        print("30 分钟无操作，已自动退出")
        return False
    LAST_ACTIVE_TIME[username] = now
    return True


def print_table(user, session):
    if not user["permissions"]:
        print("没有可查看的表权限")
        return
    print("\n可查看的表：")
    for idx, resource in enumerate(user["permissions"], start=1):
        print(f"{idx}. {resource}")
    choice = input("请选择要查看的表编号：")
    try:
        choice = int(choice) - 1
        table_name = user["permissions"][choice]
    except (ValueError, IndexError):
        print("选择无效")
        return
    model = TABLE_MAP.get(table_name)
    if not model:
        print(f"未知表 {table_name}")
        return
    rows = session.query(model).all()
    print(f"\n===== {table_name} =====")
    columns = [c.name for c in model.__table__.columns]
    for row in rows:
        row_data = ", ".join(f"{col}: {getattr(row, col)}" for col in columns)
        print(row_data)


def insert_row(user, session):
    try:
        print("\n可插入的表：")
        for idx, resource in enumerate(user["permissions"], start=1):
            print(f"{idx}. {resource}")
        choice = input("请选择要插入的表编号：")
        try:
            choice = int(choice) - 1
            table_name = user["permissions"][choice]
            if table_name in READ_ONLY_VIEWS:
                print(f"{table_name} 为只读视图，不能插入数据")
                return "error"
        except (ValueError, IndexError):
            print("选择无效")
            return "error"
        model = TABLE_MAP.get(table_name)
        if not model:
            print("未知表")
            return "error"
        columns = [c for c in model.__table__.columns if not c.primary_key or isinstance(c.type, Integer)]
        data = {}
        print("请依次输入以下字段值：")
        for col in columns:
            val = input(f"{col.name} ({col.type}): ")
            try:
                if isinstance(col.type, Integer):
                    val = int(val)
                elif isinstance(col.type, Numeric):
                    val = float(val)
            except ValueError:
                print(f"{col.name} 类型错误")
                return "error"
            data[col.name] = val
        row = model(**data)
        session.add(row)
        session.commit()
        print(f"{table_name} 插入成功！")
        return "success"
    except Exception as e:
        session.rollback()
        print(f"插入失败：{e}")
        return "error"


def delete_row(user, session):
    if not user["permissions"]:
        print("没有可删除的表权限")
        return "error"
    print("\n可删除的表：")
    for idx, resource in enumerate(user["permissions"], start=1):
        print(f"{idx}. {resource}")
    choice = input("请选择要删除的表编号：")
    try:
        choice = int(choice) - 1
        table_name = user["permissions"][choice]
        if table_name in READ_ONLY_VIEWS:
            print(f"{table_name} 为只读视图，不能删除数据")
            return "error"
    except (ValueError, IndexError):
        print("选择无效")
        return "error"
    model = TABLE_MAP.get(table_name)
    if not model:
        print(f"未知表 {table_name}")
        return "error"
    pk_columns = [c for c in model.__table__.columns if c.primary_key]
    if not pk_columns:
        print("该表没有主键，无法删除")
        return "error"
    filter_kwargs = {}
    for col in pk_columns:
        val = input(f"请输入 {col.name} ({col.type}) 用于删除: ")
        try:
            if isinstance(col.type, Integer):
                val = int(val)
            elif isinstance(col.type, Numeric):
                val = float(val)
        except ValueError:
            print(f"{col.name} 类型错误")
            return "error"
        filter_kwargs[col.name] = val
    try:
        row = session.query(model).filter_by(**filter_kwargs).first()
        if not row:
            print("未找到对应记录")
            return "error"
        session.delete(row)
        session.commit()
        print(f"{table_name} 删除成功！")
        return "success"
    except Exception as e:
        session.rollback()
        print(f"删除失败: {e}")
        return "error"


def update_row(user, session):
    if not user["permissions"]:
        print("没有可更新的表权限")
        return "error"
    print("\n可更新的表：")
    for idx, resource in enumerate(user["permissions"], start=1):
        print(f"{idx}. {resource}")
    choice = input("请选择要更新的表编号：")
    try:
        choice = int(choice) - 1
        table_name = user["permissions"][choice]
        if table_name in READ_ONLY_VIEWS:
            print(f"{table_name} 为只读视图，不能更新数据")
            return "error"
    except (ValueError, IndexError):
        print("选择无效")
        return "error"
    model = TABLE_MAP.get(table_name)
    if not model:
        print(f"未知表 {table_name}")
        return "error"
    pk_columns = [c for c in model.__table__.columns if c.primary_key]
    if not pk_columns:
        print("该表没有主键，无法更新")
        return "error"
    filter_kwargs = {}
    for col in pk_columns:
        val = input(f"请输入 {col.name} ({col.type}) 用于定位要更新的记录: ")
        try:
            if isinstance(col.type, Integer):
                val = int(val)
            elif isinstance(col.type, Numeric):
                val = float(val)
        except ValueError:
            print(f"{col.name} 类型错误")
            return "error"
        filter_kwargs[col.name] = val
    row = session.query(model).filter_by(**filter_kwargs).first()
    if not row:
        print("未找到对应记录")
        return "error"
    update_columns = [c for c in model.__table__.columns if not c.primary_key]
    print("请输入要更新的字段值，留空表示不修改：")
    for col in update_columns:
        val = input(f"{col.name} ({col.type}) [{getattr(row, col.name)}]: ")
        if val == "":
            continue
        try:
            if isinstance(col.type, Integer):
                val = int(val)
            elif isinstance(col.type, Numeric):
                val = float(val)
        except ValueError:
            print(f"{col.name} 类型错误")
            return "error"
        setattr(row, col.name, val)
    try:
        session.commit()
        print(f"{table_name} 更新成功！")
        return "success"
    except Exception as e:
        session.rollback()
        print(f"更新失败: {e}")
        return "error"


def query_row(user, session):
    if not user["permissions"]:
        print("没有可查询的表权限")
        return "error"
    print("\n可查询的表：")
    for idx, resource in enumerate(user["permissions"], start=1):
        print(f"{idx}. {resource}")
    choice = input("请选择要查询的表编号：")
    try:
        choice = int(choice) - 1
        table_name = user["permissions"][choice]
    except (ValueError, IndexError):
        print("选择无效")
        return "error"
    model = TABLE_MAP.get(table_name)
    if not model:
        print(f"未知表 {table_name}")
        return "error"
    filter_kwargs = {}
    print("请输入查询条件，留空表示不限制该字段：")
    for col in model.__table__.columns:
        val = input(f"{col.name} ({col.type}): ")
        if val == "":
            continue
        try:
            if isinstance(col.type, Integer):
                val = int(val)
            elif isinstance(col.type, Numeric):
                val = float(val)
        except ValueError:
            print(f"{col.name} 类型错误，跳过该条件")
            continue
        filter_kwargs[col.name] = val
    try:
        query = session.query(model)
        if filter_kwargs:
            query = query.filter_by(**filter_kwargs)
        rows = query.all()
        if not rows:
            print("未找到符合条件的记录")
            return "success"
        print(f"\n===== 查询 {table_name} =====")
        for row in rows:
            data = {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
            print(data)
        return "success"
    except Exception as e:
        print(f"查询失败: {e}")
        return "error"


if __name__ == "__main__":
    run()
