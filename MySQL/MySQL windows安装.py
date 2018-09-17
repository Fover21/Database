======MySQL安装======

版本5.7.X

MySQL服务器帮助我们来管理文件的操作

MySQL软件
    - 服务器端软件
        - 服务端程序
        - 解析指令
        - 对文件的操作
    - 客户端软件
        - 客户端程序
        - 发送指令（sql）
        - 解析指令

安装
    1 安装mysql服务器软件
    2 启动服务器端程序
    3 客户端连接服务端

    - 添加系统环境变量 D:\mysql-5.7.23-winx64\bin
    - 初始化 mysqld --initialize-insecure
    - 开启服务端 mysqld
    - 客户端连接（重新打开终端（以管理员身份））mysql -uroot -p
    - 接下来，以管理员身份运行cmd
        - 杀死服务端的进程
            tasklist |findstr mysql  查看进程号
            taskkill /F /PID 进程号
        - 安装windows服务（mysql服务端软件安装到windows）
            D:\mysql-5.7.23-winx64\bin\mysqld --install
            D:\mysql-5.7.23-winx64\bin\mysqld --remove
                - 启动服务
                    net start mysql
                - 关闭服务
                    net stop mysql
密码设置
    - use mysql;
    - update mysql.user set authentication_string =password('密码') where User='root';
    - 刷新权限 flush privileges;

破解密码
    - 先把mysql服务关闭
    - 管理员身份运行执行：mysql --skip-grant-tables   (跳过授权表)
    - 客户端连接服务器: mysql -uroot -p
    - 此时修改密码：update mysql.user set authentication_string =password('密码') where User='root';
    - 刷新权限（必须）：flush privileges;

====统一字符编码====

进入mysql客户端，执行\s 可以看编码

为了统一编码执行以下操作：
    - my.ini 文件是mysql的配置文件
        - 在D:\mysql-5.7.23-winx64 （应自身电脑，和bin目录同级）文件在创建my.ini文件
        - 将如下代码拷贝保存
            #mysql5.5以上：修改方式为
                [mysqld]
                character-set-server=utf8
                collation-server=utf8_general_ci
                [client]
                default-character-set=utf8
                [mysql]
                default-character-set=utf8
        - 以管理员身份重启服务
            - net stop mysql
            - net startmysql
        - 登录mysql执行\s命令查看字符集是否更改

































