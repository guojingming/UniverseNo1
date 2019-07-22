import detection_server
from threading import Thread
import config as cfg


class CharsingController:
    def __init__(self):
        self.cmd = 0
        self.ds = detection_server.DetectionServer(cfg.server_address, cfg.server_port)

    def start(self):
        self.ds.start()
        # 0:停止  1:前进  2:后退  3:左转  4:右转  5:无目标
        thread = Thread(self.process_tags, args=(1, ))
        thread.start()

    def process_tags(self):
        while True:
            flag = False
            tags = self.ds.get_tags()
            for i in range(len(tags)):
                tag = tags[i]
                type_str, x0, y0, x1, y1 = parse_tag(tag)
                if type_str == cfg.target:
                    flag = True
                    if (x0 + x1) / 2 < cfg.window_width / 2 - 100:
                        self.cmd = 3
                    elif (x0 + x1) / 2 > cfg.window_width / 2 + 100:
                        self.cmd = 4
                    else:
                        self.cmd = 1
                    break
            if flag:
                self.cmd = 5

    def get_cmd(self):
        return self.cmd


def parse_tag(tag):
    return tag[0], tag[1], tag[2], tag[3], tag[4]
