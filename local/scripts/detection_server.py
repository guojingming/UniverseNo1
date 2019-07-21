import os
from socket import *


class DetectionServer:
    def init(self, host, port, buffer_size=1024):
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = buffer_size
        self.ADDR = (self.HOST, self.PORT)
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)

    def listen(self):
        self.tcpSerSock.bind(self.ADDR)  # 绑定地址
        self.tcpSerSock.listen(5)  # 规定传入连接请求的最大数，异步的时候适用

    def close(self):
        self.tcpCliSock.close()
        self.tcpSerSock.close()

    def start(self):
        while True:
            #print('waiting for connection...')
            self.tcpCliSock, addr = self.tcpSerSock.accept()
            #print ('...connected from:', addr)
            while True:
                data = self.tcpCliSock.recv(self.BUFSIZE)
                #print("recv:", data.decode("utf-8"))
                if not data:
                    break
                filename = data.decode("utf-8")
                if os.path.exists(filename):
                    filesize = str(os.path.getsize(filename))
                    #print("文件大小为：", filesize)
                    self.tcpCliSock.send(filesize.encode())
                    data = self.tcpCliSock.recv(self.BUFSIZE)   #挂起服务器发送，确保客户端单独收到文件大小数据，避免粘包
                    print("开始发送")
                    f = open(filename, "rb")
                    for line in f:
                        self.tcpCliSock.send(line)
                else:
                    self.tcpCliSock.send("0001".encode())   #如果文件不存在，那么就返回该代码
