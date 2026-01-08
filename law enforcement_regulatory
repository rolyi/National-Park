create table 执法调度信息
(
调度编号 int primary key,
调度时间 datetime not null,
响应时间 datetime,
处置完成时间 datetime,
调度状态 varchar(10) not null default '待响应' check (调度状态 in ('待响应','已派单','已完成'))
);

create table 视频监控点信息
(
监控点编号 int primary key,
区域编号 int not null,
经度 numeric(9,6) not null,
纬度 numeric(9,6) not null,
设备状态 varchar(5) not null default '正常' check (设备状态 in ('正常','故障')),
监控范围 text not null,
数据存储周期 varchar(10) not null
);

create table 违法行为记录
(
记录编号 int primary key,
监控点编号 int,
行为类型 varchar(50) not null,
发生时间 datetime not null,
影像证据路径 text not null,
处理状态 varchar(10) not null default '未处理' check (处理状态 in ('未处理','处理中','已结案')),
处理结果 text,
处罚依据 text,
foreign key(监控点编号) references 视频监控点信息(监控点编号)
);

create table 执法人员信息
(
执法ID int primary key,
调度编号 int not null,
记录编号 int not null,
姓名 varchar(50) not null,
部门 varchar(50) not null,
权限 text not null,
联系方式 varchar(20) not null,
执法设备编号 int not null,
foreign key (调度编号) references 执法调度信息(调度编号),
foreign key (记录编号) references 违法行为记录(记录编号)
);
