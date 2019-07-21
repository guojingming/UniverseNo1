import os, struct, array
from fcntl import ioctl
import thread
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
        self.joy_stick = '/dev/input/js0'
        self.jsdev = open(self.joy_stick, 'rb')
        self.buf = array.array('B', [0])
        # JSIOCGAXES
        ioctl(self.jsdev, 0x80016a11, self.buf)

    def update_process(self):
        while True:
            evbuf = self.jsdev.read(8)
            if evbuf:
                time, value, channel_type, channel_number = struct.unpack('IhBB', evbuf)
                # axis
                if channel_type == 2:
                    # l-left or l-right
                    if channel_number == 4:
                        if value * 1.0 / 32767 <= -0.5:
                            self.cmd = 3
                        elif value * 1.0 / 32767 >= 0.5:
                            self.cmd = 4
                        else:
                            self.cmd = 0
                    elif channel_number == 5:
                        if value * 1.0 / 32767 <= -0.5:
                            self.cmd = 2
                        elif value * 1.0 / 32767 >= 0.5:
                            self.cmd = 1
                        else:
                            self.cmd = 0

    def start_joy_contoller(self):
        thread.start_new_thread(self.update_process, ("Thread-1", 2,))
