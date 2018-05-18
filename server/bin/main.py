#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com

import os
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.socket_server import server_ftp


if __name__ == "__main__":
    server = server_ftp("0.0.0.0",6969)
    while True:
        try:
            server.server_done()
        except (BrokenPipeError,ConnectionResetError) as e:
            print("客户端 Ctrl+C 断开链接......",e,"正在等待新的连接......")
            continue

