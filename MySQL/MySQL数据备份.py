============Mysql数据备份==========

1、物理备份：直接复制数据库文件，适用于大型数据库环境。但不能恢复到异构系统中如Windows
2、逻辑备份：备份的是建表、建库、插入等操作所执行的SQL语句。适用于中小型数据库，效率相对较低。
3、导出表：将表导入到文本文件中

一、使用mysqldump实现逻辑备份

#语法：
mysqldump -h 服务器 -u用户名 -p密码 数据库名 > 备份文件.sql

#示例

#单库备份
mysqldump -uroot -p123 db1 > db1.sql
mysqldump -uroot -p123 db1 table1 table2 > db1-table1-table2.sql

#多库备份
mysqldump -uroot -p123 --database db1 db2 mysql db3 > db1_db2_mysql_db3.sql

#备份所有库
mysqldump -uroot -p123 --all-database > all.sql


二、恢复逻辑备份

方法一
[root@wzy test] mysql -uroot -p123 < /test/all.sql


方法二
#方法二：
mysql> use db1;
mysql> SET SQL_LOG_BIN=0;
mysql> source /root/db1.sql

#注：如果备份/恢复单个库时，可以修改sql文件
DROP database if exists school;
create database school;
use school;





三、备份/恢复案例


#数据库备份/恢复实验一：数据库损坏
备份：
1. # mysqldump -uroot -p123 --all-databases > /backup/`date +%F`_all.sql
2. # mysql -uroot -p123 -e 'flush logs' //截断并产生新的binlog
3. 插入数据 //模拟服务器正常运行
4. mysql> set sql_log_bin=0; //模拟服务器损坏
mysql> drop database db;

恢复：
1. # mysqlbinlog 最后一个binlog > /backup/last_bin.log
2. mysql> set sql_log_bin=0; 
mysql> source /backup/2014-02-13_all.sql //恢复最近一次完全备份 
mysql> source /backup/last_bin.log //恢复最后个binlog文件


#数据库备份/恢复实验二：如果有误删除
备份：
1. mysqldump -uroot -p123 --all-databases > /backup/`date +%F`_all.sql
2. mysql -uroot -p123 -e 'flush logs' //截断并产生新的binlog
3. 插入数据 //模拟服务器正常运行
4. drop table db1.t1 //模拟误删除
5. 插入数据 //模拟服务器正常运行

恢复：
1. # mysqlbinlog 最后一个binlog --stop-position=260 > /tmp/1.sql 
# mysqlbinlog 最后一个binlog --start-position=900 > /tmp/2.sql 
2. mysql> set sql_log_bin=0; 
mysql> source /backup/2014-02-13_all.sql //恢复最近一次完全备份
mysql> source /tmp/1.log //恢复最后个binlog文件
mysql> source /tmp/2.log //恢复最后个binlog文件

注意事项：
1. 完全恢复到一个干净的环境（例如新的数据库或删除原有的数据库）
2. 恢复期间所有SQL语句不应该记录到binlog中



四、实现自动化备份


备份计划：
1. 什么时间 2:00
2. 对哪些数据库备份
3. 备份文件放的位置

备份脚本：
[root@egon ~]# vim /mysql_back.sql
#!/bin/bash
back_dir=/backup
back_file=`date +%F`_all.sql
user=root
pass=123

if [ ! -d /backup ];then
mkdir -p /backup
fi

# 备份并截断日志
mysqldump -u${user} -p${pass} --events --all-databases > ${back_dir}/${back_file}
mysql -u${user} -p${pass} -e 'flush logs'

# 只保留最近一周的备份
cd $back_dir
find . -mtime +7 -exec rm -rf {} \;

手动测试：
[root@egon ~]# chmod a+x /mysql_back.sql 
[root@egon ~]# chattr +i /mysql_back.sql
[root@egon ~]# /mysql_back.sql

配置cron：
[root@egon ~]# crontab -l
2 * * * /mysql_back.sql


五、表的导入导出

SELECT... INTO OUTFILE 导出文本文件
示例：
mysql> SELECT * FROM school.student1
INTO OUTFILE 'student1.txt'
FIELDS TERMINATED BY ',' //定义字段分隔符
OPTIONALLY ENCLOSED BY '”' //定义字符串使用什么符号括起来
LINES TERMINATED BY '\n' ; //定义换行符


mysql 命令导出文本文件
示例:
# mysql -u root -p123 -e 'select * from student1.school' > /tmp/student1.txt
# mysql -u root -p123 --xml -e 'select * from student1.school' > /tmp/student1.xml
# mysql -u root -p123 --html -e 'select * from student1.school' > /tmp/student1.html

LOAD DATA INFILE 导入文本文件
mysql> DELETE FROM student1;
mysql> LOAD DATA INFILE '/tmp/student1.txt'
INTO TABLE school.student1
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '”'
LINES TERMINATED BY '\n';


--报错：Variable 'secure_file_priv' is a read only

#可能会报错
mysql> select * from db1.emp into outfile 'C:\\db1.emp.txt' fields terminated by ',' lines terminated by '\r\n';
ERROR 1238 (HY000): Variable 'secure_file_priv' is a read only variable


#数据库最关键的是数据，一旦数据库权限泄露，那么通过上述语句就可以轻松将数据导出到文件中然后下载拿走，因而mysql对此作了限制，只能将文件导出到指定目录
在配置文件中
[mysqld]
secure_file_priv='C:\\' #只能将数据导出到C:\\下

重启mysql
重新执行上述语句



六、数据库迁移

务必保证在相同版本之间迁移
# mysqldump -h 源IP -uroot -p123 --databases db1 | mysql -h 目标IP -uroot -p456
