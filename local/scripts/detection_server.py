import os
from socket import *
from threading import Thread
import config as cfg
import camera
import numpy as np


def recv_handler(cli_socket, count):
    buf = b''
    while count:
        newbuf = cli_socket.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


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
            cap = camera.camera_init(0)
            while True:
                #get pic
                frame = camera.get_picture(cap)
                frame_string = frame.tostring()
                length = len(frame_string)
                tcpCliSock.send(str(length).ljust(16))
                tcpCliSock.send(frame_string)
                tag_data = recv_handler(tcpCliSock, 1024)

            camera.camera_release(cap)


    def start(self):
        thread = Thread(target=self.process())
        thread.start()

    def get_tags(self):
        return self.tags