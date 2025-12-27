create table 物种信息
(
物种编号 int primary key,
中文名称 varchar(50) not null,
拉丁名 varchar(50) not null,
物种分类 text not null,
保护级别 varchar(10) not null default '无' check (保护级别 in ('国家一级','国家二级','无')),
生存习性 text not null,
分布范围 text not null
);

create table 监测记录
(
记录编号 int primary key,
物种编号 int not null,
监测设备编号 int not null,
监测时间 datetime not null,
经度 numeric(9,6) not null,
纬度 numeric(9,6) not null,
监测方式 varchar(10) not null default '人工巡查' check (监测方式 in ('红外相机','人工巡查','无人机')),
监测内容 text not null,
记录人ID int not null,
数据状态 varchar(10) not null default '待核实' check (数据状态 in ('有效','待核实')),
分析结论 text,
foreign key (物种编号) references 物种信息(物种编号)
);

create table 栖息地信息
(
栖息地编号 int primary key,
区域名称 varchar(50) not null,
生态类型 varchar(20) not null,
面积 numeric(5,1) not null,
核心保护范围 text not null
);

create table 物种信息_栖息地信息_栖息
(
物种编号 int,
栖息地编号 int,
环境适应性评分 int not null check (环境适应性评分>=0 and 环境适应性评分<=100),
primary key (物种编号,栖息地编号),
foreign key (物种编号) references 物种信息(物种编号),
foreign key (栖息地编号) references 栖息地信息(栖息地编号)
);
