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

HOST = 0
PORT = 0
BUFSIZE = 0
ADDR = ()
#tcpSerSock = 0
#tcpCliSock = 0
tags = np.array([])
tcpSerSock = socket(AF_INET, SOCK_STREAM)

HOST = cfg.server_address
PORT = cfg.server_port
BUFSIZE = 1024
ADDR = (HOST, PORT)
tags = np.array([])

tcpSerSock.bind(ADDR)  # 绑定地址
tcpSerSock.listen(5)  # 规定传入连接请求的最大数，异步的时候适用

def close(tcpSerSock, tcpCliSock):
    tcpCliSock.close()
    tcpSerSock.close()

def process():
    # wrong
    tcpCliSock, addr = tcpSerSock.accept()
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
            tcpCliSock.send(str(length).encode().ljust(16))
            #print("send pic length finished")
            tcpCliSock.send(frame_string)
            #print("send frame string finished")
            tag_length = recv_handler(tcpCliSock, 16)
            tag_length = int(tag_length)
            #print("tag length: {0}".format(tag_length))
            tag_data = recv_handler(tcpCliSock, tag_length)
            #print("tag data: {0}".format(tag_data))
            tag_data = np.frombuffer(tag_data, np.int32)
            if tag_length != 0:
                tags = tag_data.reshape((-1, 5))
            print("recv tag_data finished")
        except Exception as e:
            print("exception:")
            print(e)
            break
    close(tcpSerSock, tcpCliSock)
    camera.camera_release(cap)


def start():
    thread = Thread(target=process())
    thread.setDaemon(True)
    thread.start()


def get_tags():
    return tags

