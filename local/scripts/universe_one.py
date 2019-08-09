from detection_server import DetectionServer
import config as cfg

import threading
import time

detection_server = DetectionServer(cfg.server_address, cfg.server_port)
detection_server.start()
while True:
    print(detection_server.get_tags())


# def process():
#     while True:
#         print("%s" % threading.current_thread().name)
#
#
# if __name__ == '__main__':
#     for i in range(10):
#         t = threading.Thread(target=process)
#         t.start()
#     while True:
#         print("aaaaaaaaaaaaaaaaaaaaaa")