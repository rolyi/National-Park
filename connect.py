from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from datetime import datetime, timedelta
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

    物种编号 = Column(Integer, ForeignKey("物种 信息.物种编号"), primary_key=True)
    栖息地编号 = Column(Integer, ForeignKey("栖息地信息.栖息地编号"), primary_key=True)
    环境适应性评分 = Column(Integer, nullable=False)

class 生态监测员_日常(Base):
    __tablename__ = "生态监测员_日常"
    记录编号 = Column(Integer, primary_key=True)
    物种编号 = Column(Integer)
    中文名称 = Column(String(50))
    拉丁名 = Column(String(50))
    物种分类 = Column(Text)
    保护级别 = Column(String(10))
    栖息地编号 = Column(Integer)
    区域名称 = Column(String(50))
    生态类型 = Column(String(20))
    监测设备编号 = Column(Integer)
    监测时间 = Column(DateTime)
    监测方式 = Column(String(10))
    监测内容 = Column(Text)
    经度 = Column(Numeric(9,6))
    纬度 = Column(Numeric(9,6))
    记录人ID = Column(Integer)
    数据状态 = Column(String(10))
    分析结论 = Column(Text)


class 生态监测员_待核实(Base):
    __tablename__ = "生态监测员_待核实"
    记录编号 = Column(Integer, primary_key=True)
    监测时间 = Column(DateTime)
    监测方式 = Column(String(10))
    监测内容 = Column(Text)
    经度 = Column(Numeric(9,6))
    纬度 = Column(Numeric(9,6))
    数据状态 = Column(String(10))
    分析结论 = Column(Text)


class 数据分析师_生物多样性分析(Base):
    __tablename__ = "数据分析师_生物多样性分析"
    记录编号 = Column(Integer, primary_key=True)
    中文名称 = Column(String(50))
    生存习性 = Column(Text)
    分布范围 = Column(Text)
    监测时间 = Column(DateTime)
    经度 = Column(Numeric(9,6))
    纬度 = Column(Numeric(9,6))
    区域名称 = Column(String(50))
    生态类型 = Column(String(20))
    监测内容 = Column(Text)
    分析结论 = Column(Text)

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

    # 刷新活跃时间
    LAST_ACTIVE_TIME[username] = now
    return True

TABLE_MAP=({
    "物种信息": 物种信息,
    "监测记录": 监测记录,
    "栖息地信息": 栖息地信息,
    "物种信息－栖息地信息－栖息": 物种栖息关系,
    "生态监测员_日常": 生态监测员_日常,
    "生态监测员_待核实": 生态监测员_待核实,
    "数据分析师_生物多样性分析": 数据分析师_生物多样性分析
})

READ_ONLY_VIEWS = {
    "生态监测员_日常",
    "生态监测员_待核实",
    "数据分析师_生物多样性分析"
}

def login(username: str, password: str):
    now = datetime.now()

    if username in LOCK_UNTIL:
        if now < LOCK_UNTIL[username]:
            remain = int((LOCK_UNTIL[username] - now).total_seconds())
            print(f"账户已锁定，请 {remain} 秒后再试")
            return None
        else:
            # 解锁
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

        # ===== 3️⃣ 登录成功，清状态 =====
        LOGIN_FAIL_COUNT[username] = 0
        LAST_ACTIVE_TIME[username] = now

        # ===== 4️⃣ 查角色 =====
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
                .join(
                    role_permissions,
                    Permission.id == role_permissions.permission_id
                )
                .filter(role_permissions.role_id.in_(role_ids))
                .distinct()
                .all()
            )

        return {
            "user_id": user.id,
            "username": user.username,
            "roles": [r.role_name for r in roles],
            "permissions": [p.resource for p in permissions],
            "login_time": now
        }

def print_table(user, session):
    if not user["permissions"]:
        print("没有可查看的表权限")
        return

    # 列出用户可查看的表
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

    # 查询并打印表内容
    rows = session.query(model).all()
    print(f"\n===== {table_name} =====")
    columns = [c.name for c in model.__table__.columns]  # 按表定义顺序
    for row in rows:
        row_data = ", ".join(f"{col}: {getattr(row, col)}" for col in columns)
        print(row_data)

def insert_row(user, session):
    try:
        # 选择表
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

        # 获取列信息，排除内部属性（_ 开头）
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
                # 其他类型可以按需转换
            except ValueError:
                print(f"{col.name} 类型错误")
                return "error"

            data[col.name] = val

        # 执行插入
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

    # 列出用户可删除的表
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

    # 获取主键列
    pk_columns = [c for c in model.__table__.columns if c.primary_key]
    if not pk_columns:
        print("该表没有主键，无法删除")
        return "error"

    # 如果是复合主键，多次输入
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

    # 执行删除
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

    # 列出用户可更新的表
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

    # 获取主键列
    pk_columns = [c for c in model.__table__.columns if c.primary_key]
    if not pk_columns:
        print("该表没有主键，无法更新")
        return "error"

    # 输入主键定位记录
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

    # 列出可更新的列（排除主键）
    update_columns = [c for c in model.__table__.columns if not c.primary_key]

    print("请输入要更新的字段值，留空表示不修改：")
    for col in update_columns:
        val = input(f"{col.name} ({col.type}) [{getattr(row, col.name)}]: ")
        if val == "":
            continue  # 不修改
        try:
            if isinstance(col.type, Integer):
                val = int(val)
            elif isinstance(col.type, Numeric):
                val = float(val)
            # 其他类型按需转换
        except ValueError:
            print(f"{col.name} 类型错误")
            return "error"
        setattr(row, col.name, val)

    # 执行更新
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

    # 列出用户可查询的表
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

    # 输入查询条件（可多字段）
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
            # 其他类型按需转换
        except ValueError:
            print(f"{col.name} 类型错误，跳过该条件")
            continue
        filter_kwargs[col.name] = val

    # 执行查询
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
            else:
                print("选择无效")




def run():
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

if __name__ == "__main__":
    run()
