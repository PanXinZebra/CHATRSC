# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 09:24:18 2025

@author: panxinpower
"""

import zmq;
from ZZChat import *;


# 创建ZeroMQ上下文
context = zmq.Context()
# 创建应答者套接字
socket = context.socket(zmq.REP)
# 绑定到指定地址和端口
socket.bind("tcp://localhost:5557")


zzchat=Chatter();

print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print(f"Char-RSC service started!")

while True:
    # 接收请求消息
    request = socket.recv_string()
    
    
    querystr=request;
    print(f"Receive:{querystr}");
    resultstr=zzchat.Chat(querystr);
    
    # 准备响应消息
    response = resultstr;
    # 发送响应消息
    socket.send_string(response)

