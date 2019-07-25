# coding: utf-8

from __future__ import division, print_function

import cv2
import numpy as np
import config as cfg
import socket
from yolo_utils import yolo_util as yu

param = yu.init_params("../../")


def recv_handler(cli_socket, count):
    buf = b''
    while count:
        newbuf = cli_socket.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf




class RemoteClient:
    def __init__(self):
        self.cli_socket = socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.cli_socket.connect((cfg.server_address, cfg.server_port))

    def process(self):
        while 1:
            length = recv_handler(self.cli_socket, 16)
            string_data = recv_handler(self.cli_socket, int(length))
            data = np.frombuffer(string_data, np.uint8)
            img_ori = cv2.imdecode(data, cv2.IMREAD_COLOR)
            height_ori, width_ori = img_ori.shape[:2]
            img_ori, boxes_, scores_, labels_ = yu.get_predict_result(img_ori, param)
            # reconstruct result
            result = np.concatenate((boxes_[:, 0:4], np.zeros((len(boxes_), 1))), axis=1)
            result = result.astype(int)
            for i in range(len(boxes_)):
                result[i, -1] = labels_[i]
            result = result.reshape((-1))
            result_string = result.tostring()
            print("resultString: " + str(result))
            print("length: {0}".format(len(result_string)))
            self.cli_socket.send(str.encode(str(len(result_string)).ljust(16)))
            self.cli_socket.send(result_string)

    #def start(self):

