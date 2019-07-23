import os
from socket import *
from threading import Thread

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

    def process(self):
        # wrong
        while True:
            self.tags = []
            self.tcpCliSock, addr = self.tcpSerSock.accept()
            while True:
                data = self.tcpCliSock.recv(self.BUFSIZE)
                if not data:
                    break
                filename = data.decode("utf-8")
                if os.path.exists(filename):
                    filesize = str(os.path.getsize(filename))
                    self.tcpCliSock.send(filesize.encode())
<<<<<<< HEAD
                    data = self.tcpCliSock.recv(self.BUFSIZE)   #挂起服务器发送，确保客户端单独收到文件大小数据，避免粘包
                    #print("开始发送")
=======
                    data = self.tcpCliSock.recv(self.BUFSIZE)  # 挂起服务器发送，确保客户端单独收到文件大小数据，避免粘包
                    print("开始发送")
>>>>>>> ce14f2df50fc28e62af5f65fe28f8b19f558e1f1
                    f = open(filename, "rb")
                    for line in f:
                        self.tcpCliSock.send(line)
                else:
                    self.tcpCliSock.send("0001".encode())  # 如果文件不存在，那么就返回该代码

    def start(self):
        thread = Thread(target=self.process())
        thread.start()

    def get_tags(self):
        return self.tags