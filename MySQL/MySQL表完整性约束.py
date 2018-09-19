=======MySQL表完整性约束======

目录：
	一、介绍
	二、not null 与 default
	三、unique
	四、primary key
	五、auto_increment
	六、foreign key


一、介绍
	约束条件与数据类型的宽度一样，都是可选参数
	作用：用于保证数据的完整性和一致性

	主要分为：
		PRIMARY KEY (PK) 标识该字段为表的主键，可以唯一的标识记录
		FOREIGN KEY (FK) 标识该字段为该表的外键
		NOT NULL  标识该字段不能为空
		UNIQUE KEY (UK)  标识该字段是唯一值
		AUTO_INCREMENT 标识该字段的值自动增长（整数类型，而且为主键）
		DEFAULT  为该字段设置默认值

		UNSIGNED  无符号
		ZEROFILL  使用0填充


	说明：
		1. 是否允许为空，默认NULL，可设置NOT NULL，字段不允许为空，必须赋值
		2. 字段是否有默认值，缺省的默认值是NULL，如果插入记录时不给字段赋值，此字段使用默认值
		sex enum('male','female') not null default 'male'
		age int unsigned NOT NULL default 20 必须为正值（无符号） 不允许为空 默认是20
		3. 是否是key
		主键 primary key
		外键 foreign key
		索引 (index,unique...)

二、not null与default

		是否为空,null表示空,非字符串
		not null  -不可空
		null      -可空

		默认值，创建列时可以指定默认值，当插入数据时如果未主动设置，则自动添加默认值
		create table tb1(
			nid int not null defalut 2,
			num int not null
		)

三、unique
	============设置唯一约束 UNIQUE===============
		方法一：
		create table department1(
		id int,
		name varchar(20) unique,
		comment varchar(100)
		);


		方法二：
		create table department2(
			id int,
			name varchar(20),
			comment varchar(100),
			constraint uk_name unique(name)  #为唯一索引起名字
		);

		注：唯一联合
			create table service(
				id int primary key auto_increment,
				name varchar(20),
				host varchar(15) not null,
				port int not null,
				unique(host,port) #联合唯一
			);


四、primary
	从约束角度看primary key字段的值不为空且唯一，那我们直接使用not null+unique不就可以了吗，要它干什么？
	主键primary key是innodb存储引擎组织数据的依据，innodb称之为索引组织表，一张表中必须有且只有一个主键。

	一个表中可以：
		单列做主键
		多列做主键（复合主键）

		- 单列做主键
			============单列做主键===============
			#方法一：not null+unique
			create table department1(
			id int not null unique, #主键
			name varchar(20) not null unique,
			comment varchar(100)
			);

			mysql> desc department1;
			+---------+--------------+------+-----+---------+-------+
			| Field   | Type         | Null | Key | Default | Extra |
			+---------+--------------+------+-----+---------+-------+
			| id      | int(11)      | NO   | PRI | NULL    |       |
			| name    | varchar(20)  | NO   | UNI | NULL    |       |
			| comment | varchar(100) | YES  |     | NULL    |       |
			+---------+--------------+------+-----+---------+-------+
			rows in set (0.01 sec)

			#方法二：在某一个字段后用primary key
			create table department2(
			id int primary key, #主键
			name varchar(20),
			comment varchar(100)
			);

			mysql> desc department2;
			+---------+--------------+------+-----+---------+-------+
			| Field   | Type         | Null | Key | Default | Extra |
			+---------+--------------+------+-----+---------+-------+
			| id      | int(11)      | NO   | PRI | NULL    |       |
			| name    | varchar(20)  | YES  |     | NULL    |       |
			| comment | varchar(100) | YES  |     | NULL    |       |
			+---------+--------------+------+-----+---------+-------+
			rows in set (0.00 sec)

			#方法三：在所有字段后单独定义primary key
			create table department3(
			id int,
			name varchar(20),
			comment varchar(100),
			constraint pk_name primary key(id); #创建主键并为其命名pk_name

			mysql> desc department3;
			+---------+--------------+------+-----+---------+-------+
			| Field   | Type         | Null | Key | Default | Extra |
			+---------+--------------+------+-----+---------+-------+
			| id      | int(11)      | NO   | PRI | NULL    |       |
			| name    | varchar(20)  | YES  |     | NULL    |       |
			| comment | varchar(100) | YES  |     | NULL    |       |
			+---------+--------------+------+-----+---------+-------+
			rows in set (0.01 sec)

		- 多列做主键
			==================多列做主键================
			create table service(
			ip varchar(15),
			port char(5),
			service_name varchar(10) not null,
			primary key(ip,port)
			);


			mysql> desc service;
			+--------------+-------------+------+-----+---------+-------+
			| Field        | Type        | Null | Key | Default | Extra |
			+--------------+-------------+------+-----+---------+-------+
			| ip           | varchar(15) | NO   | PRI | NULL    |       |
			| port         | char(5)     | NO   | PRI | NULL    |       |
			| service_name | varchar(10) | NO   |     | NULL    |       |
			+--------------+-------------+------+-----+---------+-------+
			3 rows in set (0.00 sec)

			mysql> insert into service values
			    -> ('172.16.45.10','3306','mysqld'),
			    -> ('172.16.45.11','3306','mariadb')
			    -> ;
			Query OK, 2 rows affected (0.00 sec)
			Records: 2  Duplicates: 0  Warnings: 0

			mysql> insert into service values ('172.16.45.10','3306','nginx');
			ERROR 1062 (23000): Duplicate entry '172.16.45.10-3306' for key 'PRIMARY'


五、auto_increment
	- 约束字段为自增长，被约束的字段必须同时被key约束
		- 不指定id，则自动增长
		- 也可以指定id
		- 对于自增的字段，在用delete删除后，再插入值，该字段仍按照删除前的位置继续增长
		- 应该用truncate清空表，比起delete一条一条地删除记录，truncate是直接清空表，在删除大表时用它


	- 步长:auto_increment_increment,起始偏移量:auto_increment_offset
		#在创建完表后，修改自增字段的起始值
		mysql> create table student(
		    -> id int primary key auto_increment,
		    -> name varchar(20),
		    -> sex enum('male','female') default 'male'
		    -> );

		mysql> alter table student auto_increment=3;

		mysql> show create table student;
		.......
		ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8

		mysql> insert into student(name) values('jake');
		Query OK, 1 row affected (0.01 sec)

		mysql> select * from student;
		+----+------+------+
		| id | name | sex  |
		+----+------+------+
		|  3 | jake | male |
		+----+------+------+
		row in set (0.00 sec)

		mysql> show create table student;
		.......
		ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8


		#也可以创建表时指定auto_increment的初始值，注意初始值的设置为表选项，应该放到括号外
		create table student(
		id int primary key auto_increment,
		name varchar(20),
		sex enum('male','female') default 'male'
		)auto_increment=3;




		#设置步长
		sqlserver：自增步长
		    基于表级别
		    create table t1（
		        id int。。。
		    ）engine=innodb,auto_increment=2 步长=2 default charset=utf8

		mysql自增的步长：
		    show session variables like 'auto_inc%';
		    
		    #基于会话级别
		    set session auth_increment_increment=2 #修改会话级别的步长

		    #基于全局级别的
		    set global auth_increment_increment=2 #修改全局级别的步长（所有会话都生效）


		#！！！注意了注意了注意了！！！
		If the value of auto_increment_offset is greater than that of auto_increment_increment, the value of auto_increment_offset is ignored. 
		翻译：如果auto_increment_offset的值大于auto_increment_increment的值，则auto_increment_offset的值会被忽略 ，这相当于第一步步子就迈大了，扯着了蛋
		比如：设置auto_increment_offset=3，auto_increment_increment=2




		mysql> set global auto_increment_increment=5;
		Query OK, 0 rows affected (0.00 sec)

		mysql> set global auto_increment_offset=3;
		Query OK, 0 rows affected (0.00 sec)

		mysql> show variables like 'auto_incre%'; #需要退出重新登录
		+--------------------------+-------+
		| Variable_name            | Value |
		+--------------------------+-------+
		| auto_increment_increment | 1     |
		| auto_increment_offset    | 1     |
		+--------------------------+-------+



		create table student(
		id int primary key auto_increment,
		name varchar(20),
		sex enum('male','female') default 'male'
		);

		mysql> insert into student(name) values('jake1'),('jake2'),('jake3');
		mysql> select * from student;
		+----+-------+------+
		| id | name  | sex  |
		+----+-------+------+
		|  3 | jake1 | male |
		|  8 | jake2 | male |
		| 13 | jake3 | male |
		+----+-------+------+

六、foreign key
	- 快速理解foreign key
		员工信息表有三个字段：工号  姓名  部门
		公司有3个部门，但是有1个亿的员工，那意味着部门这个字段需要重复存储，部门名字越长，越浪费

		解决方法：
			我们完全可以定义一个部门表
			然后让员工信息表关联该表，如何关联，即foreign key

		#表类型必须是innodb存储引擎，且被关联的字段，即references指定的另外一个表的字段，必须保证唯一
		create table department(
		id int primary key,
		name varchar(20) not null
		)engine=innodb;

		#dpt_id外键，关联父表（department主键id），同步更新，同步删除
		create table employee(
		id int primary key,
		name varchar(20) not null,
		dpt_id int,
		constraint fk_name foreign key(dpt_id)
		references department(id)
		on delete cascade
		on update cascade 
		)engine=innodb;

		#先往父表department中插入记录
		#再往子表employee中插入记录
		#删父表department，子表employee中对应的记录跟着删
		#更新父表department，子表employee中对应的记录跟着改
	- 如何找出两张表中的关系
		分析步骤：
		#1、先站在左表的角度去找
		是否左表的多条记录可以对应右表的一条记录，如果是，则证明左表的一个字段foreign key 右表一个字段（通常是id）

		#2、再站在右表的角度去找
		是否右表的多条记录可以对应左表的一条记录，如果是，则证明右表的一个字段foreign key 左表一个字段（通常是id）

		#3、总结：
		#多对一：
		如果只有步骤1成立，则是左表多对一右表
		如果只有步骤2成立，则是右表多对一左表

		#多对多
		如果步骤1和2同时成立，则证明这两张表时一个双向的多对一，即多对多,需要定义一个这两张表的关系表来专门存放二者的关系

		#一对一:
		如果1和2都不成立，而是左表的一条记录唯一对应右表的一条记录，反之亦然。这种情况很简单，就是在左表foreign key右表的基础上，将左表的外键字段设置成unique即可

	- 建立表之间的关系
		#一对多或称为多对一
		三张表：出版社，作者信息，书

		一对多（或多对一）：一个出版社可以出版多本书

		关联方式：foreign key

			=====================多对一=====================
			create table press(
			id int primary key auto_increment,
			name varchar(20)
			);

			create table book(
			id int primary key auto_increment,
			name varchar(20),
			press_id int not null,
			foreign key(press_id) references press(id)
			on delete cascade
			on update cascade
			);



		#多对多
		三张表：出版社，作者信息，书

		多对多：一个作者可以写多本书，一本书也可以有多个作者，双向的一对多，即多对多
		　　
		关联方式：foreign key+一张新的表

			=====================多对多=====================
			create table author(
			id int primary key auto_increment,
			name varchar(20)
			);


			#这张表就存放作者表与书表的关系，即查询二者的关系查这表就可以了
			create table author2book(
			id int not null unique auto_increment,
			author_id int not null,
			book_id int not null,
			constraint fk_author foreign key(author_id) references author(id)
			on delete cascade
			on update cascade,
			constraint fk_book foreign key(book_id) references book(id)
			on delete cascade
			on update cascade,
			primary key(author_id,book_id)
			);



		#一对一
		两张表：学生表和客户表

		一对一：一个学生是一个客户，一个客户有可能变成一个学校，即一对一的关系

		关联方式：foreign key+unique

			=====================一对一=====================
			#一定是student来foreign key表customer，这样就保证了：
			#1 学生一定是一个客户，
			#2 客户不一定是学生，但有可能成为一个学生


			create table customer(
			id int primary key auto_increment,
			name varchar(20) not null,
			qq varchar(10) not null,
			phone char(16) not null
			);


			create table student(
			id int primary key auto_increment,
			class_name varchar(20) not null,
			customer_id int unique, #该字段一定要是唯一的
			foreign key(customer_id) references customer(id) #外键的字段一定要保证unique
			on delete cascade
			on update cascade
			);

