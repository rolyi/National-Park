from sqlalchemy import Column, String, Date, DateTime, CheckConstraint, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# 科研项目信息模型
class ResearchProject(Base):
    __tablename__ = 'research_project'
    __table_args__ = (
        CheckConstraint("project_status IN ('在研', '已结题', '暂停')", name='ck_project_status'),
        {'comment': '科研项目信息表'}
    )
    
    project_id = Column(String(20), primary_key=True, comment='项目编号')
    project_name = Column(String(100), nullable=False, comment='项目名称')
    director_id = Column(String(20), nullable=False, comment='负责人ID')
    apply_unit = Column(String(50), nullable=False, comment='申请单位')
    approve_date = Column(Date, nullable=False, comment='立项时间')
    finish_date = Column(Date, nullable=True, comment='结题时间')
    project_status = Column(String(10), nullable=False, comment='项目状态')
    research_field = Column(String(30), nullable=False, comment='研究领域')
    
    # 关联采集记录和成果
    data_collections = relationship('ResearchDataCollection', backref='project', cascade='all, delete-orphan')
    achievements = relationship('ResearchAchievement', backref='project', cascade='all, delete-orphan')

# 科研数据采集记录模型
class ResearchDataCollection(Base):
    __tablename__ = 'research_data_collection'
    __table_args__ = (
        CheckConstraint("data_source IN ('实地采集', '系统调用')", name='ck_data_source'),
        Index('idx_collection_project', 'project_id'),  # 索引
        {'comment': '科研数据采集记录表'}
    )
    
    collection_id = Column(String(20), primary_key=True, comment='采集编号')
    project_id = Column(String(20), ForeignKey('research_project.project_id', ondelete='CASCADE'), nullable=False, comment='项目编号')
    collector_id = Column(String(20), nullable=False, comment='采集人ID')
    collection_time = Column(DateTime, nullable=False, comment='采集时间')
    area_id = Column(String(20), nullable=False, comment='区域编号')
    collection_content = Column(String(200), nullable=False, comment='采集内容')
    data_source = Column(String(20), nullable=False, comment='数据来源')

# 科研成果信息模型
class ResearchAchievement(Base):
    __tablename__ = 'research_achievement'
    __table_args__ = (
        CheckConstraint("share_permission IN ('公开', '内部共享', '保密')", name='ck_share_permission'),
        Index('idx_achievement_project', 'project_id'),  # 索引
        {'comment': '科研成果信息表'}
    )
    
    achievement_id = Column(String(20), primary_key=True, comment='成果编号')
    project_id = Column(String(20), ForeignKey('research_project.project_id', ondelete='CASCADE'), nullable=False, comment='项目编号')
    achievement_type = Column(String(20), nullable=False, comment='成果类型')
    achievement_name = Column(String(100), nullable=False, comment='成果名称')
    publish_date = Column(Date, nullable=False, comment='发表/提交时间')
    share_permission = Column(String(10), nullable=False, comment='共享权限')
    file_path = Column(String(200), nullable=False, comment='文件路径')
