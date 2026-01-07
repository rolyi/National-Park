from datetime import date, datetime
from models.research_models import ResearchProject, ResearchDataCollection, ResearchAchievement
from dao.research_dao import init_tables, ResearchProjectDAO, ResearchDataCollectionDAO, ResearchAchievementDAO

# 初始化表
init_tables()

# 测试1：新增科研项目
project = ResearchProject(
    project_id="RP006",
    project_name="珍稀鸟类栖息地保护研究",
    director_id="U009",
    apply_unit="北京林业大学生态学院",
    approve_date=date(2024, 4, 1),
    finish_date=None,
    project_status="在研",
    research_field="物种保护"
)
success, msg = ResearchProjectDAO.add_project(project)
print(f"新增项目结果：{success} - {msg}")

# 测试2：查询项目
project = ResearchProjectDAO.get_project_by_id("RP006")
if project:
    print(f"查询到项目：{project.project_name}（状态：{project.project_status}）")

# 测试3：新增采集记录
collection = ResearchDataCollection(
    collection_id="RC006",
    project_id="RP006",
    collector_id="U010",
    collection_time=datetime(2024, 4, 10, 9, 0, 0),
    area_id="A004",
    collection_content="鸟类数量统计（编号：BD001-BD030）",
    data_source="实地采集"
)
success, msg = ResearchDataCollectionDAO.add_collection(collection)
print(f"新增采集记录结果：{success} - {msg}")

# 测试4：新增科研成果
achievement = ResearchAchievement(
    achievement_id="RA006",
    project_id="RP002",
    achievement_type="论文",
    achievement_name="东北虎保护技术综述",
    publish_date=date(2024, 8, 1),
    share_permission="公开",
    file_path="/data/achievement/paper/RP002_002.pdf"
)
success, msg = ResearchAchievementDAO.add_achievement(achievement)
print(f"新增成果结果：{success} - {msg}")

# 测试5：按状态查询项目
ongoing_projects = ResearchProjectDAO.get_projects_by_status("在研")
print(f"在研项目数量：{len(ongoing_projects)}")
for p in ongoing_projects[:2]:  # 只打印前2个
    print(f"- {p.project_id}：{p.project_name}")
