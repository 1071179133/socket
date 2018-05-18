#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import sys
import socket
import hashlib
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import read_and_write_file as rw
from lib.logger import logger

user_file = "../db/user.json"

class server_ftp(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server = socket.socket()    #声明socket类型，同时生成socket连接对象
        self.server.bind((self.host,self.port)) #绑定地址端口
        self.server.listen(5) #开始监听,最大允许5个连接排队
        logger.info("等待连接：")

    #@login("chenjianwen","123456")
    def server_done(self):
        while True:
            data = rw.read(user_file)
            user_status = False
            m = hashlib.md5()
            conn,addr = self.server.accept()  ##阻塞状态，等待连接进来...
            logger.info("连接来了.....")
            while True:
                if not user_status:
                    user = conn.recv(1024).decode("utf-8")        #接收客户端输入的用户名  数据包大小：官方建议最大8192（8k）
                    conn.send("get user".encode("utf-8"))        #回应一下已收到用户名
                    passwd = conn.recv(1024).decode("utf-8")      #接收客户端输入的密码
                    conn.send("get passwd".encode("utf-8"))      #回应一下已收到密码
                    print(user,passwd)
                    user_dir = os.path.join(os.getcwd(),"..","user_home","%s")%user
                    #print(user_dir)
                    if not os.path.exists(user_dir):            #如果登陆用户的目录不存在，则创建
                        os.makedirs(user_dir)
                    try:
                        password = data[user]["passwd"]
                    except KeyError as e:
                        exit("用户名或密码错误...")
                    if data[user] and passwd == password:           #验证账号密码是否正确
                        logger.info("user:[%s],addr:[%s],login susess...."%(user,addr))
                        user_status = True
                if user_status:
                    cmd = None
                    filename = None
                    data = None
                    cmd = conn.recv(1024).decode("utf-8")     #接收需要执行的命令
                    print(cmd)
                    if not cmd:continue
                    conn.sendall("ack server: get cmd".encode("utf-8"))     #回应客户端已收到需要执行的命令
                    if cmd == "q":
                        logger.info("user:[%s],addr:[%s],连接断开....."%(user,addr))
                        break
                    elif "get" in cmd:
                        filename = conn.recv(1024).decode("utf-8")    #接收文件名称
                        conn.sendall("get filename".encode("utf-8"))    #回应客户端已收到文件名称
                        conn.recv(1024)     ##接收客户端说可以开始发送数据的指示
                        logger.info("user:[%s],addr:[%s],get [%s]"%(user,addr,filename))
                        file = "%s/%s"%(user_dir,filename)
                        if os.path.isfile(file):
                            file_size = str(os.stat(file).st_size).encode("utf-8")      ##获取文件大小，转换为二进制
                            conn.send(file_size)            ##发送文件大小给客户端
                            f = open(file,"rb")
                            for line in f:
                                m.update(line)
                                conn.send(line)                            #发送对应文件数据到客户端
                            file_md5 = m.hexdigest()                   #获取文件的MD5值
                            conn.send(file_md5.encode("utf-8"))        #发送MD5值
                            logger.info("user:[%s],addr:[%s],下载文件[%s]成功" %(user,addr,filename))
                            f.close()
                        else:
                            file_size = str("0").encode("utf-8")  ##获取文件大小，转换为二进制
                            conn.send(file_size)  ##发送文件大小给客户端
                            print("文件不存在")
                    elif "push" in cmd:
                        filename = conn.recv(1024).decode("utf-8")    #若果是上传，则接收第二条数据，接收文件数据
                        conn.send("get filename".encode("utf-8"))    #回应客户端已收到文件名称
                        logger.info("user:[%s],addr:[%s],push [%s]"%(user,addr,filename))
                        file_size = int(conn.recv(1024).decode("utf-8"))     #接收上传的文件大小
                        conn.send("I get file_size".encode("utf-8"))
                        recv_size = 0
                        f = open("%s/%s" % (user_dir, filename), 'wb')
                        while recv_size < file_size:
                            if file_size - recv_size > 1024:
                                size = 1024
                            else:
                                size = file_size - recv_size
                            data = conn.recv(size)                        #接收客户端传过来的文件数据
                            m.update(data)
                            recv_size += len(data)
                            f.write(data)
                        else:
                            client_file_md5 = conn.recv(1024).decode("utf-8")  # 接收服务端发来的MD5
                            recv_file_md5 = m.hexdigest()
                            if client_file_md5 == recv_file_md5:
                                print("已校验MD5值，上传成功")
                                conn.send("已校验MD5值，上传成功".encode("utf-8"))
                            else:
                                print("MD5值校验失败，文件数据有错，上传失败")
                                conn.send("MD5值校验失败，文件数据有错，上传失败".encode("utf-8"))
                            f.close()

                    elif "push" not in cmd and "get" not in cmd:
                        conn.recv(1024)     #接收客户端可以执行的信号
                        if cmd == "ls" or cmd == "dir":         #判断执行那种命令
                            cmd_list = "%s %s"%(cmd,user_dir)
                            print(cmd_list)
                            msg = os.popen("%s %s"%(cmd,user_dir)).read()
                        else:
                            msg = os.popen(cmd).read()
                        #print(msg)
                        if msg:
                            msg_size = str(len(msg)).encode("utf-8")     ###获取结果长度
                            conn.send(msg_size)                 ##发送长度给客户端
                            conn.recv(1024)                 ##接收客户端的回应，他已收到长度了
                            conn.sendall(msg.encode("utf-8"))           #发送执行结果内容给客户端
                            logger.info("user:[%s],addr:[%s],执行命令[%s]" %(user,addr,cmd))
                        else:
                            msg = "执行命令错误"
                            msg_size = str(len(msg)).encode("utf-8")  ###获取结果长度
                            conn.send(msg_size)  ##发送长度给客户端
                            conn.recv(1024)  ##接收客户端的回应，他已收到长度了
                            conn.sendall(msg.encode("utf-8"))
                            logger.info("user:[%s],addr:[%s],执行命令出错或命令不存在，[%s]"%(user,addr,cmd))
                            continue
                    else:
                        logger.error("user:[%s],addr:[%s],不符合命令要求.....断开"%(user,addr))
                        break