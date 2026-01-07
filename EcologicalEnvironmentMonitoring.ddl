create table 监测指标信息
(
指标编号 int primary key,
指标名称 varchar(20) not null,
计量单位 varchar(20) not null,
阈值上限 numeric(5,1) not null,
阈值下限 numeric(5,1) not null,
监测频率 varchar(10)
);

create table 环境监测数据
(
数据编号 int primary key,
采集时间 datetime not null,
数据质量 varchar(10) not null check 
    (数据质量 in ('优','良','中','差')) 
);

create table 监测设备信息
(
设备编号 int primary key,
设备类型 varchar(20) not null,
安装时间 datetime not null,
校准周期 varchar(10) not null,
校准记录 text not null,
通信协议 varchar(20) not null,
运行状态 varchar(10) not null check
    (运行状态 in ('正常','故障','离线')) 
);

create table 监测指标信息_环境监测数据_关联
(
指标编号 int,
数据编号 int,
primary key (指标编号,数据编号),
foreign key (指标编号) references 监测指标信息(指标编号),
foreign key (数据编号) references 环境监测数据(数据编号)
);

create table 环境监测数据_监测设备信息_监测
(
数据编号 int,
设备编号 int,
监测值 numeric(5,1) not null,
区域编号 int not null,
功能分区 varchar(20) not null,
primary key (数据编号,设备编号),
foreign key (数据编号) references 环境监测数据(数据编号),
foreign key (设备编号) references 监测设备信息(设备编号)
);
