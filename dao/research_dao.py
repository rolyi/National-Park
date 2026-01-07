from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.research_models import Base, ResearchProject, ResearchDataCollection, ResearchAchievement
from config import DB_URL

# 创建引擎和会话
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)

# 初始化数据表（首次运行时执行）
def init_tables():
    """创建科研数据支撑业务线的所有表"""
    Base.metadata.create_all(engine)
    print("科研数据支撑业务线数据表创建成功！")

# 科研项目相关操作
class ResearchProjectDAO:
    @staticmethod
    def add_project(project: ResearchProject):
        """新增科研项目"""
        with Session() as session:
            try:
                session.add(project)
                session.commit()
                return True, "项目新增成功"
            except Exception as e:
                session.rollback()
                return False, f"新增失败：{str(e)}"

    @staticmethod
    def get_project_by_id(project_id: str):
        """根据项目编号查询项目"""
        with Session() as session:
            return session.query(ResearchProject).filter_by(project_id=project_id).first()

    @staticmethod
    def update_project_status(project_id: str, new_status: str):
        """更新项目状态"""
        with Session() as session:
            try:
                project = session.query(ResearchProject).filter_by(project_id=project_id).first()
                if not project:
                    return False, "项目不存在"
                project.project_status = new_status
                session.commit()
                return True, "状态更新成功"
            except Exception as e:
                session.rollback()
                return False, f"更新失败：{str(e)}"

    @staticmethod
    def get_projects_by_status(status: str):
        """按状态查询项目列表"""
        with Session() as session:
            return session.query(ResearchProject).filter_by(project_status=status).all()

# 科研数据采集记录相关操作
class ResearchDataCollectionDAO:
    @staticmethod
    def add_collection(collection: ResearchDataCollection):
        """新增采集记录"""
        with Session() as session:
            try:
                # 校验项目是否存在且未结题
                project = session.query(ResearchProject).filter_by(project_id=collection.project_id).first()
                if not project:
                    return False, "关联的项目不存在"
                if project.project_status == '已结题':
                    return False, "项目已结题，不可新增采集记录"
                session.add(collection)
                session.commit()
                return True, "采集记录新增成功"
            except Exception as e:
                session.rollback()
                return False, f"新增失败：{str(e)}"

    @staticmethod
    def get_collections_by_project(project_id: str):
        """查询某项目的所有采集记录"""
        with Session() as session:
            return session.query(ResearchDataCollection).filter_by(project_id=project_id).all()

# 科研成果相关操作
class ResearchAchievementDAO:
    @staticmethod
    def add_achievement(achievement: ResearchAchievement):
        """新增科研成果"""
        with Session() as session:
            try:
                session.add(achievement)
                session.commit()
                return True, "成果新增成功"
            except Exception as e:
                session.rollback()
                return False, f"新增失败：{str(e)}"

    @staticmethod
    def get_achievements_by_permission(permission: str):
        """按共享权限查询成果"""
        with Session() as session:
            return session.query(ResearchAchievement).filter_by(share_permission=permission).all()
