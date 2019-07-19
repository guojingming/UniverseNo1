# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array
from fcntl import ioctl

joy_stick = '/dev/input/js0'
jsdev = open(joy_stick, 'rb')

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES

#Type 1:Button   2:axis
#Number <=> Channel Number

#Mapping Tbale：
#
#Value    Type    Number    Comment
#-32767   2       0         left
#32767    2       0         right
#-32767   2       1         up
#32767    2       1         down
#-32767   2       4         l-left
#32767    2       4         l-right
#-32767   2       5         l-up
#32767    2       5         l-down

while True:
    evbuf = jsdev.read(8)
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)
        #print(str(value) + " " + str(type) + " " + str(number))
        if type == 2:#axis
            if number == 4:#l-left or l-right
                if value * 1.0 / 32767 <= -0.5:
                
                elif value * 1.0 / 32767 >= 0.5:

                else:

            elif number == 5:
		if value * 1.0 / 32767 <= -0.5:
                
                elif value * 1.0 / 32767 >= 0.5:

                else:


