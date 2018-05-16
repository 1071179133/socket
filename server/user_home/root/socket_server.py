#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import socket
#from login import login
from lib import read_and_write_file as rw

user_file = "./db/user.json"

class server_ftp(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server = socket.socket()    #声明socket类型，同时生成socket连接对象
        self.server.bind((self.host,self.port)) #绑定地址端口
        self.server.listen(5) #开始监听,最大允许5个连接排队
        print("等待连接：")

    #@login("chenjianwen","123456")
    def server_done(self):
        while True:
            data = rw.read(user_file)
            user_status = False
            conn,addr = self.server.accept()
            print("连接来了.....")
            while True:
                if not user_status:
                    user = conn.recv(102400).decode("utf-8")        #接收客户端输入的用户名
                    #conn.sendall("get user".encode("utf-8"))        #回应一下已收到用户名
                    passwd = conn.recv(102400).decode("utf-8")      #接收客户端输入的密码
                    #conn.sendall("get passwd".encode("utf-8"))      #回应一下已收到密码
                    print(user,passwd)
                    user_dir = "./%s"%user
                    if not os.path.exists(user_dir):            #如果登陆用户的目录不存在，则创建
                        os.makedirs(user_dir)
                    try:
                        password = data[user]["passwd"]
                    except KeyError as e:
                        exit("用户名或密码错误...")
                    if data[user] and passwd == password:           #验证账号密码是否正确
                        print("[%s],login susess...." % user)
                        user_status = True
                if user_status:
                    cmd = None
                    filename = None
                    data = None
                    cmd = conn.recv(102400).decode("utf-8")     #接收需要执行的命令
                    print(cmd)
                    if not cmd:continue
                    #conn.sendall("get cmd".encode("utf-8"))     #回应客户端已收到需要执行的命令
                    if cmd == "q":
                        print("连接断开.....")
                        break
                    elif "get" in cmd:
                        filename = conn.recv(102400).decode("utf-8")    #接收文件名称
                        #conn.sendall("get filename".encode("utf-8"))    #回应客户端已收到文件名称
                        print("client:",addr,"get [%s]"%filename)
                        f = open("%s/%s"%(user_dir,filename),"rb")
                        f_data = f.read()
                        conn.sendall(f_data)                            #发送对应文件数据到客户端
                        print(addr, "下载文件[%s]成功" % filename)
                        f.close()
                    elif "push" in cmd:
                        filename = conn.recv(102400).decode("utf-8")    #若果是上传，则接收第二条数据，接收文件数据
                        conn.sendall("get filename".encode("utf-8"))    #回应客户端已收到文件名称
                        print("client:", addr, "push [%s]" %filename)
                        data = conn.recv(102400)                        #接收客户端传过来的文件数据
                        f = open("%s/%s"%(user_dir,filename), 'wb')
                        f.write(data)
                        print(addr, "上传文件[%s]成功"%filename)
                        f.close()
                    elif "push" not in cmd and "get" not in cmd:
                        msg = os.popen("%s %s"%(cmd,user_dir)).read()
                        if msg:
                            conn.sendall(msg.encode("utf-8"))           #发送执行结果内容给客户端
                            print("执行命令[%s]" % cmd)
                        else:
                            conn.sendall("执行命令错误".encode("utf-8"))
                            print("执行命令出错或命令不存在，[%s]"%cmd)
                            continue
                    else:
                        print("不符合命令要求.....断开")
                        break

if __name__ == "__main__":
    server = server_ftp("0.0.0.0",6969)
    server.server_done()
