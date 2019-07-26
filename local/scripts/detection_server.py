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
    def __init__(self, host, port, buffer_size=1024):
        self.HOST = host
        self.PORT = port
        self.BUFSIZE = buffer_size
        self.ADDR = (self.HOST, self.PORT)
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tags = np.array([])

    def listen(self):
        self.tcpSerSock.bind(self.ADDR)  # 绑定地址
        self.tcpSerSock.listen(5)  # 规定传入连接请求的最大数，异步的时候适用

    def close(self):
        self.tcpCliSock.close()
        self.tcpSerSock.close()

    def process(self):
        self.listen()
        # wrong
        self.tcpCliSock, addr = self.tcpSerSock.accept()
        print("connetion builded")
        cap = camera.camera_init(0)
        print("carmera opened")
        while True:
            #get pic
            try:
                res, frame = camera.get_picture(cap)
                frame_string = frame.tostring()
                #print("pic_data got")
                length = len(frame_string)
                self.tcpCliSock.send(str(length).encode().ljust(16))
                #print("send pic length finished")
                self.tcpCliSock.send(frame_string)
                #print("send frame string finished")
                tag_length = recv_handler(self.tcpCliSock, 16)
                tag_length = int(tag_length)
                #print("tag length: {0}".format(tag_length))
                tag_data = recv_handler(self.tcpCliSock, tag_length)
                #print("tag data: {0}".format(tag_data))
                tag_data = np.frombuffer(tag_data, np.int32)
                if tag_length != 0:
                    self.tags = tag_data.reshape((-1, 5))
                print("recv tag_data finished")
            except Exception as e:
                print("exception:")
                print(e)
                break
        self.close()
        camera.camera_release(cap)


    def start(self):
        thread = Thread(target=self.process())
        thread.setDaemon(True)
        thread.start()


    def get_tags(self):
        return self.tags


if __name__ == '__main__':
    detection_server = DetectionServer(cfg.server_address, cfg.server_port)
    detection_server.start()
    while True:
        print(detection_server.get_tags())
