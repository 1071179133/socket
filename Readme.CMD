1.程序文件及说明：
socket							#项目根目录
|-- client						#客户端模块目录
|   `-- socket_client.py		#客户端运行程序
`-- server						#服务端端模块目录
    |-- bin						#服务端执行目录
    |   `-- main.py				#服务端程序入口
    |-- core					#服务端核心代码目录
    |   `-- socket_server.py	#服务端核心代码程序
    |-- db						#用户数据目录
    |   `-- user.json			#用户数据库
    |-- lib						#公共模块工具
    |   |-- get_list.py			#未使用
    |   |-- init_db_dir.py		#未使用
    |   |-- logger.py			#日志模块
    |   |-- login.py			#登陆模块，未使用
    |   `-- read_and_write_file.py	#读写json文件模块
    |-- log						#存放日志目录
    |   |-- access.log			#最新日志文件
    |   `-- access.log.2018-05-11
    |   `-- login.cpython-35.pyc
    `-- user_home				#用户家目录
        |-- chenjianwen			#用户chenjianwen家目录
        `-- root				#用户root家目录

2.python版本：python-3.5.3

3.程序使用：
	服务端：cd socket/server/bin/ && python main.py
	客户端：cd socket/client/ &&  python socket_client.py 根据提示使用程序

4.github项目地址：https://github.com/1071179133/socket.git