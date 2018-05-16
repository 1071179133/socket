#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import socket

class client_ftp(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.client = socket.socket()  # 声明socket类型，同时生成socket连接对象
        try:
            self.client.connect((self.host,self.port))
        except ConnectionRefusedError as e:
            print("目标计算机积极拒绝，无法连接", e)
        print("""
默认账号密码：
    username：root
    password：123
        """)
        self.user = input("username：").strip()
        self.passwd = input("password：").strip()
        self.client.sendall(self.user.encode("utf-8"))  # 发送user给服务端
        self.client.sendall(self.passwd.encode("utf-8"))  # 发送passwd给服务端

    def done_cmd(self,cmd):
        #self.client.sendall(self.user.encode("utf-8"))      #发送user给服务端
        #user_c = self.client.recv(102400)                   #接收服务端的回应
        #self.client.sendall(self.passwd.encode("utf-8"))    #发送passwd给服务端
        #passwd_c = self.client.recv(102400)                 #接收服务端的回应
        self.client.sendall(cmd.encode("utf-8"))            #发动执行命令给服务端
        data = self.client.recv(102400)                     #接收命令执行的返回结果
        data = data.decode()
        print(data)

    def get_file(self,cmd):
        #self.client.sendall(self.user.encode("utf-8"))      #发送user给服务端
        #user_c = self.client.recv(102400)                   #接收服务端的回应
        #self.client.sendall(self.passwd.encode("utf-8"))    #发送passwd给服务端
        #passwd_c = self.client.recv(102400)                 #接收服务端的回应

        msg_cmd = cmd.split(' ')[0]
        msg_filename = cmd.split(' ')[1]
        self.client.sendall(msg_cmd.encode("utf-8"))
        #data = self.client.recv(102400)
        self.client.sendall(msg_filename.encode("utf-8"))
        data = self.client.recv(102400)
        f = open(msg_filename,'wb')
        if f.write(data):
            print("文件[%s]下载成功"%msg_filename)
        f.close()

    def push_file(self,cmd):
        #self.client.sendall(self.user.encode("utf-8"))      #发送user给服务端
        #user_c = self.client.recv(102400)                   #接收服务端的回应
        #self.client.sendall(self.passwd.encode("utf-8"))    #发送passwd给服务端
        #passwd_c = self.client.recv(102400)                 #接收服务端的回应

        msg_cmd = cmd.split(' ')[0]
        print(msg_cmd)
        self.client.sendall(msg_cmd.encode("utf-8"))
        #data = self.client.recv(102400)
        msg_filename = cmd.split(' ')[1]
        print(msg_filename)
        self.client.sendall(msg_filename.encode("utf-8"))
        data = self.client.recv(102400)
        f = open(msg_filename, 'rb')
        data = f.read()
        self.client.sendall(data)
        print("上传文件[%s]成功"%msg_filename)
        f.close()

    def logout(self,cmd):
        print("退出ftp客户端....")
        self.client.sendall(cmd.encode("utf-8"))

if __name__ == "__main__":
    client = client_ftp('127.0.0.1', 6969)
    print("""=========使用说明=========
    ls/dir           #查看目录下文件列表
    get filename     #下载文件
    push filename    #上传文件
    q                #退出客户端
    说明：当用户目录文件下没有文件存在时，不能使用 ls/dir 命令
    问题：目前不支持传输大数据文件
    """)
    while True:
        cmd = input("FTP_CLIENT#")
        if not cmd:continue
        if cmd == 'q':
            client.logout(cmd)
            break
        elif cmd and "get" in cmd:
            client.get_file(cmd)
        elif cmd and "push" in cmd:
            client.push_file(cmd)
        elif "push" not in cmd and "get" not in cmd:
            client.done_cmd(cmd)
        else:
            print("输入有误.....")
            continue
