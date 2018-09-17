======权限管理======

我们知道我们的最高权限管理者是root用户，它拥有着最高的权限操作。包括select、update、delete、update、grant等操作。
那么一般情况在公司之后DBA工程师会创建一个用户和密码，让你去连接数据库的操作，并给当前的用户设置某个操作的权限（或者所有权限）。
那么这时就需要我们来简单了解一下：

如何创建用户和密码
给当前的用户授权
移除当前用户的权限
如果你想创建一个新的用户，则需要以下操作：

    1- 进入到mysql数据库下
        use mysql;
    2- 对新用户增删改
        -1 创建用户
            - 指定ip：192.118.1.1的wzy用户登录
                - create user 'wzy'@'192.118.1.1' identified by '123';
            - 指定ip：192.118.1.开头的wzy用户登录
                - create user 'wzy'@'192.118.1.%' identified by '123';
            - 指定任何ip的wzy用户
                - create user 'wzy'@'%' identified by '123';
        -2 删除用户
            - drop user '用户名'@'IP地址';
        -3 修改用户
            - rename user '用户名'@'IP地址' to '新用户名'@'IP地址';
        -4 修改密码
            - set password for '用户名'@'IP地址'=Password('新密码');
    3- 对当前的用户授权管理
        -1 查看授权
            - show grants for '用户'@'IP地址'
        -2 给权限
            -1 授权wzy用户仅对db1.t1文件有查询、插入、和更新的操作
                - grant select ,insert,update on db1.t1 to "wzy"@'%';
            -2 表示有所有的权限，除了grant这个命令，这个命令是root才有的。wzy用户对db1下的t1文件有任意操作
                - grant all privileges  on db1.t1 to "wzy"@'%';
            -3 wzy用户对db1数据库中的文件执行任何操作
                - grant all privileges  on db1.* to "wzy"@'%';
            -4 wzy用户对所用数据库中文件有任何操作
                - grant all privileges  on *.*  to "wzy"@'%';
        -3 取消权限
            -1 取消wzy用户对db1的t1文件的任意权限
                - revoke all on db1.t1 from 'wzy'@"%";
            -2 取消来自远程服务器的wzy用户对数据库db1的所有表的所有权限
                - revoke all on db1.* from 'wzy'@"%";
            -3 取消来自远程服务器的wzy用户所有数据库的所有表权限
                - revoke all privileges on *.* from 'wzy'@'%';
    4- MySQL备份命令行操作
        1- 备份
            -1 备份：数据库表结构+数据
            - mysqdump -u root db1 > db1.sql -p
            -2 备份：数据表结构
            - mysqdump -u root -d db1 > db1.sql -p
        2- 导入现有的数据到某个数据库
            -1 先创建一个新的数据库
                - reate database db10;
            -2 将已有的数据库文件导入到db10数据库中
                - mysqdump -u root -d db10 < db1.sql -p
