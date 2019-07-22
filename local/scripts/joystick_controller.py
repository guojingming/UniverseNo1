import os, struct, array
from fcntl import ioctl
from threading import Thread
import time


'''
Type 1:Button   2:axis
Number <=> Channel Number
Mapping Tbale：
Value    Type    Number    Comment
-32767   2       0         left
32767    2       0         right
-32767   2       1         up
32767    2       1         down
-32767   2       4         l-left
32767    2       4         l-right
-32767   2       5         l-up
32767    2       5         l-down
'''


class JoystickController:
    def __init__(self):
        # 0:stop 1:forward 2:backward 3:turn_left 4:turn_right
        self.cmd = 0
        # 0:待机模式 1:遥控 2:追踪
        self.mode = 0
        self.joy_stick = '/dev/input/js1'
        self.jsdev = open(self.joy_stick, 'rb')
        self.buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a11, self.buf)

    def update_process(self):
        while True:
            evbuf = self.jsdev.read(8)
            if evbuf:
                time, value, channel_type, channel_number = struct.unpack('IhBB', evbuf)
                print(str(channel_type) + " " + str(channel_number) + " " + str(value))
                # axis
                if channel_type == 2:
                    # l-left or l-right
                    if channel_number == 6:
                        if value * 1.0 / 32767 <= -0.1:
                            self.cmd = 3
                        elif value * 1.0 / 32767 >= 0.1:
                            self.cmd = 4
                        else:
                            self.cmd = 0
                    elif channel_number == 7:
                        if value * 1.0 / 32767 <= -0.5:
                            self.cmd = 1
                            continue
                        elif value * 1.0 / 32767 >= 0.5:
                            self.cmd = 2
                            continue
                        else:
                            self.cmd = 0
                            continue
                elif channel_type == 1:
                    # 待机
                    if channel_number == 0:
                        if value == 1:
                            self.mode = 0
                    # 遥控
                    if channel_number == 2:
                        if value == 1:
                            self.mode = 1

                    # 追踪
                    if channel_number == 1:
                        if value == 1:
                            self.mode = 2

    def start_joy_contoller(self):
        thread = Thread(target=self.update_process)
        thread.start()

    def get_cmd(self):
        return self.cmd

    def get_mode(self):
        return self.mode


if __name__ == "__main__":
    jc = JoystickController()
    jc.start_joy_contoller()
    while True:
        print(str(jc.get_cmd()) + " " + str(jc.get_mode()))
