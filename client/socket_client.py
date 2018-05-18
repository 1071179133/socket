#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import socket
import hashlib

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
        self.client.recv(1024)          #服务端收到user回应
        self.client.sendall(self.passwd.encode("utf-8"))  # 发送passwd给服务端
        self.client.recv(1024)  # 服务端收到passwd回应
        self.m = hashlib.md5()

    def done_cmd(self,cmd):
        self.client.sendall(cmd.encode("utf-8"))            #发动执行命令给服务端
        self.client.recv(1024)                              #接收服务端返回ack信号，说明它已收到执行命令
        self.client.send("you can done and send data to me".encode("utf-8"))  ##提示服务端可以开始执行命令并发送数据了
        msg_size = int(self.client.recv(1024).decode("utf-8"))             #接收返回结果的长度
        self.client.send("Client Already Get The Msg Length!".encode("utf-8"))
        recv_size = 0
        recv_data = ""
        while recv_size < msg_size:
            if msg_size - recv_size > 1024:
                size = 1024
            else:
                size = msg_size - recv_size
            data = self.client.recv(1024).decode()               #接收命令执行的返回结果
            recv_size += len(data)
            recv_data += data
        print(recv_data)

    def get_file(self,cmd):
        msg_cmd = cmd.split(' ')[0]
        msg_filename = cmd.split(' ')[1]
        self.client.sendall(msg_cmd.encode("utf-8"))
        self.client.recv(1024)      ##接收服务端回应说收到执行指令
        self.client.sendall(msg_filename.encode("utf-8"))
        self.client.recv(1024)  ##接收服务端回应说收到执行文件名了
        self.client.send("you can send data to me".encode("utf-8"))        ##提示服务端可以开始发送数据了
        file_size = int(self.client.recv(1024).decode("utf-8"))      #接收文件数据的大小
        #print(file_size)
        if file_size != 0:
            print("文件执行下载....")
            recv_file_size = 0
            f = open(msg_filename, 'wb')
            while recv_file_size < file_size:   #当接收到的数据大小小于文件数据总大小
                if file_size - recv_file_size > 1024:   #表是不是最后一次接收                         ##解决粘包问题
                    size = 1024
                else:                                   #小于或等于1024，表是是最后一次接收，有多少收多少         ##解决粘包问题
                    size = file_size - recv_file_size
                data = self.client.recv(size)
                self.m.update(data)
                f.write(data)
                recv_file_size += len(data)
            else:
                server_file_md5 = self.client.recv(1024).decode("utf-8")      #接收服务端发来的MD5
                recv_file_md5 = self.m.hexdigest()
                if server_file_md5 == recv_file_md5:
                    print("已校验MD5值，下载成功")
                else:
                    print("MD5值校验失败，文件数据有错，下载失败")
                f.close()
        else:
            print("文件不存在，无法下载....")

    def push_file(self,cmd):
        msg_cmd = cmd.split(' ')[0]
        print(msg_cmd)
        self.client.sendall(msg_cmd.encode("utf-8"))           #发送命令给服务端
        self.client.recv(1024)          ##服务端回应已收到cmd
        msg_filename = cmd.split(' ')[1]
        print(msg_filename)
        if os.path.isfile(msg_filename):
            self.client.sendall(msg_filename.encode("utf-8"))       #发送文件名给服务端
            self.client.recv(1024)  ##服务端回应已收到文件名
            file_size = str(os.stat(msg_filename).st_size).encode("utf-8")      ##获取文件大小，转换为二进制
            self.client.send(file_size)         ##发送文件大小给服务端
            self.client.recv(1024)      ##服务端反馈已收到文件大小信号
            f = open(msg_filename, 'rb')
            for line in f:
                self.m.update(line)
                self.client.sendall(line)
            file_md5 = self.m.hexdigest()
            self.client.send(file_md5.encode("utf-8"))
            push_status = self.client.recv(1024).decode("utf-8")
            print(push_status)
            f.close()
        else:
            print("[%s]文件不存在，无法上传..."%msg_filename)

    def logout(self,cmd):
        print("退出ftp客户端....")
        self.client.sendall(cmd.encode("utf-8"))

if __name__ == "__main__":
    client = client_ftp('127.0.0.1', 6969)
    print("""=========使用说明=========
    ls/dir           #查看目录下文件列表[windows下不支持ls命令]
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
