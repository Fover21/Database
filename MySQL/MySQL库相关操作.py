========MySQL库相关操作======

一、系统数据库

information_schema： 虚拟库，不占用磁盘空间，存储的是数据库启动后的一些参数，如用户表信息、列信息、权限信息、字符信息等
performance_schema： MySQL 5.5开始新增一个数据库：主要用于收集数据库服务器性能参数，记录处理查询请求时发生的各种事件、锁等现象 
mysql：	授权库，主要存储系统用户的权限信息
test：	MySQL数据库系统自动创建的测试数据库

二、创建数据库

	- 语法（help create database）
		- CREATE DATABASE 数据库名 charset utf8;

	- 数据库命名规则
		- 可以使用字母、数字、下划线、@、#、$
		- 区分大小写
		- 不能单独使用关键字如：create select
		- 不能单独使用数字
		- 最长128位

三、数据库相关操作

	- 查看数据库
		- show databases;
		- show create database db1;
		- select database();

	- 选择数据库
		-  USE 数据库名;

	- 删除数据库
		- DROP DATABASE 数据库名;

	- 修改数据库
		- alert database db1 charset utf8;

