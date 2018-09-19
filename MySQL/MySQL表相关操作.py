======MySQL表相关操作=====

目录：
	- 一、存储引擎介绍
	- 二、表介绍
	- 三、创建表
	- 四、查看表结构
	- 五、数据类型
	- 六、表完整性约束
	- 七、修改表ALTER TABLE
	- 八、复制表
	- 九、删除表


一、存储引擎介绍
	- 什么是存储引擎
	- MySQL支持的存储引擎
	- 使用存储引擎

存储引擎即表类型，mysql根据不同的表类型会有不同的处理机制
	- 什么是存储引擎
		mysql中建立的库===>文件夹
		库中建立的表===>文件

		现实生活中我们用来存储数据的文件有不同的类型，每种文件类型对应各自不同的处理机制：比如处理文本用txt类型，处理表格用excel，处理图片用png等
		数据库中的表也应该有不同的类型，表的类型不同，会对应mysql不同的存取机制，表类型又称为存储引擎。

		存储引擎说白了就是如何存储数据、如何为存储的数据建立索引和如何更新、查询数据等技术的实现方
		法。因为在关系数据库中数据的存储是以表的形式存储的，所以存储引擎也可以称为表类型（即存储和
		操作此表的类型）

		在Oracle 和SQL Server等数据库中只有一种存储引擎，所有数据存储管理机制都是一样的。而MySql
		数据库提供了多种存储引擎。用户可以根据不同的需求为数据表选择不同的存储引擎，用户也可以根据
		自己的需要编写自己的存储引擎

		SQL 解析器、SQL 优化器、缓冲池、存储引擎等组件在每个数据库中都存在,但不是每 个数据库都有这么
		多存储引擎。MySQL 的插件式存储引擎可以让存储引擎层的开发人员设 计他们希望的存储层,例如,有的应
		用需要满足事务的要求,有的应用则不需要对事务有这 么强的要求 ;有的希望数据能持久存储,有的只希望
		放在内存中,临时并快速地提供对数据 的查询。

	- MySQL支持的存储引擎
		- show engines\G;	#产看所有支持的存储引擎
		- show variables like 'storage_engine%'; #查看正在使用的存储引擎

		- MySQL存储引擎介绍
			- #InnoDB 存储引擎
				支持事务,其设计目标主要面向联机事务处理(OLTP)的应用。其特点是行锁设计、支持外键,并支
				持类似 Oracle 的非锁定读,即默认读取操作不会产生锁。 从 MySQL 5.5.8 版本开始是默认
				的存储引擎。InnoDB 存储引擎将数据放在一个逻辑的表空间中,这个表空间就像黑盒一样由 InnoDB
				存储引擎自身来管理。从 MySQL 4.1(包括 4.1)版本开始,可以将每个 InnoDB 存储引擎的 表单独
				存放到一个独立的 ibd 文件中。此外,InnoDB 存储引擎支持将裸设备(row disk)用 于建立其表空间。
				InnoDB 通过使用多版本并发控制(MVCC)来获得高并发性,并且实现了 SQL 标准 的 4 种隔离级别,默认
				为 REPEATABLE 级别,同时使用一种称为 netx-key locking 的策略来 避免幻读(phantom)现象的产生。
				除此之外,InnoDB 存储引擎还提供了插入缓冲(insert buffer)、二次写(double write)、自适应哈希索
				引(adaptive hash index)、预读(read ahead) 等高性能和高可用的功能。
				对于表中数据的存储,InnoDB 存储引擎采用了聚集(clustered)的方式,每张表都是按 主键的顺序进行存储的,
				如果没有显式地在表定义时指定主键,InnoDB 存储引擎会为每一 行生成一个 6 字节的 ROWID,并以此作为主键。
				InnoDB 存储引擎是 MySQL 数据库最为常用的一种引擎,Facebook、Google、Yahoo 等 公司的成功应用已经
				证明了 InnoDB 存储引擎具备高可用性、高性能以及高可扩展性。对其 底层实现的掌握和理解也需要时间和技术
				的积累。如果想深入了解 InnoDB 存储引擎的工作 原理、实现和应用,可以参考《MySQL 技术内幕:InnoDB 存储引擎》一书。

			- #MyISAM 存储引擎
				不支持事务、表锁设计、支持全文索引,主要面向一些 OLAP 数 据库应用,在 MySQL 5.5.8 版本之前是默认的存储引擎(除 Windows 版本外)。
				数据库系统 与文件系统一个很大的不同在于对事务的支持,MyISAM 存储引擎是不支持事务的。究其根 本,这也并不难理解。用户在所有的应用中
				是否都需要事务呢?在数据仓库中,如果没有 ETL 这些操作,只是简单地通过报表查询还需要事务的支持吗?此外,MyISAM 存储引擎的 另一个与众
				不同的地方是,它的缓冲池只缓存(cache)索引文件,而不缓存数据文件,这与 大多数的数据库都不相同。

			- #NDB 存储引擎
				2003 年,MySQL AB 公司从 Sony Ericsson 公司收购了 NDB 存储引擎。 NDB 存储引擎是一个集群存储引擎,类似于 Oracle 的 RAC 集群,
				不过与 Oracle RAC 的 share everything 结构不同的是,其结构是 share nothing 的集群架构,因此能提供更高级别的 高可用性。NDB 存
				储引擎的特点是数据全部放在内存中(从 5.1 版本开始,可以将非索引数 据放在磁盘上),因此主键查找(primary key lookups)的速度极快,并且
				能够在线添加 NDB 数据存储节点(data node)以便线性地提高数据库性能。由此可见,NDB 存储引擎是高可用、 高性能、高可扩展性的数据库集群
				系统,其面向的也是 OLTP 的数据库应用类型。

			- #Memory 存储引擎
				正如其名,Memory 存储引擎中的数据都存放在内存中,数据库重 启或发生崩溃,表中的数据都将消失。它非常适合于存储 OLTP 数据库应用中临时
				数据的临时表,也可以作为 OLAP 数据库应用中数据仓库的维度表。Memory 存储引擎默认使用哈希 索引,而不是通常熟悉的 B+ 树索引。

			- #Infobright 存储引擎
				第三方的存储引擎。其特点是存储是按照列而非行的,因此非常 适合 OLAP 的数据库应用。其官方网站是 http://www.infobright.org/,上面
				有不少成功的数据 仓库案例可供分析。

			- #NTSE 存储引擎
				网易公司开发的面向其内部使用的存储引擎。目前的版本不支持事务, 但提供压缩、行级缓存等特性,不久的将来会实现面向内存的事务支持。

			- #BLACKHOLE
				黑洞存储引擎，可以应用于主备复制中的分发主库。

			MySQL 数据库还有很多其他存储引擎,上述只是列举了最为常用的一些引擎。如果 你喜欢,完全可以编写专属于自己的引擎,这就是开源赋予我们的能力,也是开源的魅 力所在。


	- 使用存储引擎
		- 方法一：建表时指定
			- create table innodb_t1(id int,name char)engine=innodb;
			- create table innodb_t2(id int)engine=innodb;
			- show create table innodb_t1;
			- show create table innodb_t2;

		- 方法二：在配置文件中指定默认的存储引擎
			/etc/my.cnf
			[mysqld]
			default-storage-engine=iNNODB
			innodb_file_pre=1

二、表介绍
	
	-表相当于文件，表中的一条记录就相当于文件的一行内容，不同的是，表中的一条记录有对应的标题，称为表的字段。

三、创建表
	
	-语法
		create table 表名(
			字段名1 类型(宽度) 约束条件，
			字段名2 类型(宽度) 约束条件，
			......
			);
			注：表中最后一个字段不要加逗号

		注意：
			- 在同一张表中，字段名是不能相同
			- 宽度和约束条件可选
			- 字段名和类型是必须得

四、产看表结构
	
	- describe 表名; #查看表结构，可简写成为 desc 表名

	- show create table 表名\G;   #查看表详细结构,可加\G

五、数据类型
	- 介绍
	- 数值类型
	- 日期类型
	- 字符创类型
	- 枚举类型与集合类型


	- 介绍
		- 存储引擎决定了表的类型，而表内存放的数据也要有不同的类型，每种数据类型都有自己的宽度，但宽度是可选的

		- MySQL常用数据类型概述
			- 数字
				- 整形:tinyinit int bigint
				- 小数:
					- float:在位数比较短的情况下不准确
					- double:在位数较长的情况下不准确
					- decimal:精确（如果是小数，则推荐使用decimal）-内部原理是以字符串的形式去存

			- 字符串
				- char(10):简单粗暴，浪费空间，存储速度块   root存成root000000
				- varchar:准确，节省空间，存储速度慢
				- sql优化：
					- 创建表时，定长的类型往前放，变长的往后放
					- >255个字符，超了就把文件路径存放在数据库中

			- 时间类型
				- 最常用：datetime

			- 枚举类型与集合类型

	- 数据类型
		- 整数类型
			整数类型：TINYINT SMALLINT MEDIUMINT INT BIGINT
			作用：存储年龄，等级，id，各种号码等

			注：用zerofill测试整数类型的显示宽度

			create table t7(x int(3) zerofill);
			insert into t7 values(1),(11),(111),(1111);
			select * from t7;
			+------+
			| x    |
			+------+
			|  001 |
			|  011 |
			|  111 |
			| 1111 | #超过宽度限制仍然可以存
			+------+

			注意：为该类型指定宽度时，仅仅只是指定查询结果的显示宽度，与存储范围无关
				其实我们完全没必要为整数类型指定显示宽度，使用默认的就可以了
				默认的显示宽度，都是在最大值的基础上加1


			int的存储宽度是4个Bytes，即32个bit，即2**32
			无符号最大值为：4294967296-1
			有符号最大值：2147483648-1
			有符号和无符号的最大数字需要的显示宽度均为10，而针对有符号的最小值则需要11位才能显示完全，所以int类型默认的显示宽度为11是非常合理的
			最后：整形类型，其实没有必要指定显示宽度，使用默认的就ok

		- 浮点数
			定点数类型  DEC等同于DECIMAL　　
			浮点类型：FLOAT DOUBLE
			作用：存储薪资、身高、体重、体质参数等

		- 位类型（了解）
			BIT(M)可以用来存放多位二进制数，M范围从1~64，如果不写默认为1位。
				注意：对于位字段需要使用函数读取
    				bin()显示为二进制
    				hex()显示为十六进制

    - 日期类型
    	DATE TIME DATETIME TIMESTAMP YEAR 
		作用：存储用户注册时间，文章发布时间，员工入职时间，出生时间，过期时间等

		YEAR
            YYYY（1901/2155）

        DATE
            YYYY-MM-DD（1000-01-01/9999-12-31）

        TIME
            HH:MM:SS（'-838:59:59'/'838:59:59'）

        DATETIME

            YYYY-MM-DD HH:MM:SS（1000-01-01 00:00:00/9999-12-31 23:59:59    Y）

        TIMESTAMP

            YYYYMMDD HHMMSS（1970-01-01 00:00:00/2037 年某时）

        ============注意啦，注意啦，注意啦===========
		1. 单独插入时间时，需要以字符串的形式，按照对应的格式插入
		2. 插入年份时，尽量使用4位值
		3. 插入两位年份时，<=69，以20开头，比如50,  结果2050      
               			 >=70，以19开头，比如71，结果1971

        datetime与timestamp的区别
        
        在实际应用的很多场景中，MySQL的这两种日期类型都能够满足我们的需要，存储精度都为秒，但在某些情况下，会展现出他们各自的优劣。下面就来总结一下两种日期类型的区别。

		1.DATETIME的日期范围是1001——9999年，TIMESTAMP的时间范围是1970——2038年。
		2.DATETIME存储时间与时区无关，TIMESTAMP存储时间与时区有关，显示的值也依赖于时区。在mysql服务器，操作系统以及客户端连接都有时区的设置。
		3.DATETIME使用8字节的存储空间，TIMESTAMP的存储空间为4字节。因此，TIMESTAMP比DATETIME的空间利用率更高。
		4.DATETIME的默认值为null；TIMESTAMP的字段默认不为空（not null）,默认值为当前时间（CURRENT_TIMESTAMP），如果不做特殊处理，并且update语句中没有指定该列的更新值，则默认更新为当前时间。		 


	- 字符串类型
		#注意：char和varchar括号内的参数指的都是字符的长度

		#char类型：定长，简单粗暴，浪费空间，存取速度快
		    字符长度范围：0-255（一个中文是一个字符，是utf8编码的3个字节）
		    存储：
		        存储char类型的值时，会往右填充空格来满足长度
		        例如：指定长度为10，存>10个字符则报错，存<10个字符则用空格填充直到凑够10个字符存储

		    检索：
		        在检索或者说查询时，查出的结果会自动删除尾部的空格，除非我们打开pad_char_to_full_length SQL模式（SET sql_mode = 'PAD_CHAR_TO_FULL_LENGTH';）

		#varchar类型：变长，精准，节省空间，存取速度慢
		    字符长度范围：0-65535（如果大于21845会提示用其他类型 。mysql行最大限制为65535字节，字符编码为utf-8：https://dev.mysql.com/doc/refman/5.7/en/column-count-limit.html）
		    存储：
		        varchar类型存储数据的真实内容，不会用空格填充，如果'ab  ',尾部的空格也会被存起来
		        强调：varchar类型会在真实数据前加1-2Bytes的前缀，该前缀用来表示真实数据的bytes字节数（1-2Bytes最大表示65535个数字，正好符合mysql对row的最大字节限制，即已经足够使用）
		        如果真实的数据<255bytes则需要1Bytes的前缀（1Bytes=8bit 2**8最大表示的数字为255）
		        如果真实的数据>255bytes则需要2Bytes的前缀（2Bytes=16bit 2**16最大表示的数字为65535）
		    
		    检索：
		        尾部有空格会保存下来，在检索或者说查询时，也会正常显示包含空格在内的内容

		了解两个函数
		length：查看字节数
		char_length:查看字符数

		1. char填充空格来满足固定长度，但是在查询时却会很不要脸地删除尾部的空格（装作自己好像没有浪费过空间一样），然后修改sql_mode让其现出原形
		2. 虽然 CHAR 和 VARCHAR 的存储方式不太相同,但是对于两个字符串的比较,都只比 较其值,忽略 CHAR 值存在的右填充,即使将 SQL _MODE 设置为 PAD_CHAR_TO_FULL_ LENGTH 也一样,,但这不适用于like
		3.总结：
			#InnoDB存储引擎：建议使用VARCHAR类型
			单从数据类型的实现机制去考虑，char数据类型的处理速度更快，有时甚至可以超出varchar处理速度的50%。

			但对于InnoDB数据表，内部的行存储格式没有区分固定长度和可变长度列（所有数据行都使用指向数据列值的头指针），因此在本质上，使用固定长度的CHAR列不一定比使用可变长度VARCHAR列性能要好。
			因而，主要的性能因素是数据行使用的存储总量。由于CHAR平均占用的空间多于VARCHAR，因此使用VARCHAR来最小化需要处理的数据行的存储总量和磁盘I/O是比较好的。

			#其他字符串系列（效率：char>varchar>text）
			TEXT系列 TINYTEXT TEXT MEDIUMTEXT LONGTEXT
			BLOB 系列    TINYBLOB BLOB MEDIUMBLOB LONGBLOB 
			BINARY系列 BINARY VARBINARY

			text：text数据类型用于保存变长的大字符串，可以组多到65535 (2**16 − 1)个字符。
			mediumtext：A TEXT column with a maximum length of 16,777,215 (2**24 − 1) characters.
			longtext：A TEXT column with a maximum length of 4,294,967,295 or 4GB (2**32 − 1) characters.


	- 枚举类型与集合类型
		字段的值只能在给定范围中选择，如单选框，多选框
		enum 单选	只能在给定的范围内选一个值，如性别 sex 男male/女female
		set 多选 在给定的范围内可以选择一个或一个以上的值（爱好1,爱好2,爱好3...）

			枚举类型（enum）
            An ENUM column can have a maximum of 65,535 distinct elements. (The practical limit is less than 3000.)
            示例：
                CREATE TABLE shirts (
                    name VARCHAR(40),
                    size ENUM('x-small', 'small', 'medium', 'large', 'x-large')
                );
                INSERT INTO shirts (name, size) VALUES ('dress shirt','large'), ('t-shirt','medium'),('polo shirt','small');

  

            集合类型（set）
            A SET column can have a maximum of 64 distinct members.
            示例：
                CREATE TABLE myset (col SET('a', 'b', 'c', 'd'));
                INSERT INTO myset (col) VALUES ('a,d'), ('d,a'), ('a,d,a'), ('a,d,d'), ('d,a,d');

六、表完整性约束
	下篇单独介绍

七、修改表ALTER
	
	- 语法
		- 修改表名
			ALTER TABLE 表名 RENAME 新表明;
		- 增加字段
			ALTER TABLE 表名 ADD 字段名 数据类型 [完整性约束条件...],ADD 字段名 数据类型 [完整性约束条件];
			ALTER TABLE 表名 ADD 字段名 数据类型 [完整性约束条件...] FIRST;
			ALTER TABLE 表名 ADD 字段名 数据类型 [完整性约束条件...] AFTER 字段名;
		- 删除字段
			ALTER TABLE 表名 DROP 字段名;
		- 修改字段
			ALTER TABLE 表名 MODIFY 字段名 数据类型 [完整性约束条件...];
			ALTER TABLE 表名 CHANGE 旧字段名 新字段名 旧数据类型 [完整性约束条件...]；
			ALTER TABLE 表名 CHANGE 旧字段名 新字段名 新数据类型 [完整性约束条件...]；


		例子：
			1. 修改存储引擎
			mysql> alter table service 
			    -> engine=innodb;

			2. 添加字段
			mysql> alter table student10
			    -> add name varchar(20) not null,
			    -> add age int(3) not null default 22;
			    
			mysql> alter table student10
			    -> add stu_num varchar(10) not null after name;                //添加name字段之后

			mysql> alter table student10                        
			    -> add sex enum('male','female') default 'male' first;          //添加到最前面

			3. 删除字段
			mysql> alter table student10
			    -> drop sex;

			mysql> alter table service
			    -> drop mac;

			4. 修改字段类型modify
			mysql> alter table student10
			    -> modify age int(3);
			mysql> alter table student10
			    -> modify id int(11) not null primary key auto_increment;    //修改为主键

			5. 增加约束（针对已有的主键增加auto_increment）
			mysql> alter table student10 modify id int(11) not null primary key auto_increment;
			ERROR 1068 (42000): Multiple primary key defined

			mysql> alter table student10 modify id int(11) not null auto_increment;
			Query OK, 0 rows affected (0.01 sec)
			Records: 0  Duplicates: 0  Warnings: 0

			6. 对已经存在的表增加复合主键
			mysql> alter table service2
			    -> add primary key(host_ip,port);        

			7. 增加主键
			mysql> alter table student1
			    -> modify name varchar(10) not null primary key;

			8. 增加主键和自动增长
			mysql> alter table student1
			    -> modify id int not null primary key auto_increment;

			9. 删除主键
			a. 删除自增约束
			mysql> alter table student10 modify id int(11) not null; 

			b. 删除主键
			mysql> alter table student10                                 
			    -> drop primary key;

八、复制表
	- 复制表结构＋记录 （key不会复制: 主键、外键和索引）
		mysql> create table new_service select * from service;

		只复制表结构
		mysql> select * from service where 1=2;        //条件为假，查不到任何记录
		Empty set (0.00 sec)
		mysql> create table new1_service select * from service where 1=2;  
		Query OK, 0 rows affected (0.00 sec)
		Records: 0  Duplicates: 0  Warnings: 0

		mysql> create table t4 like employees;


九、删除表

	- DROP TABLE 表名;









