import RPi.GPIO as GPIO
import os, struct, array
from fcntl import ioctl
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
#GPIO.setup(27,GPIO.OUT)
#GPIO.setup(22,GPIO.OUT)
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
					GPIO.output(17,False)
					GPIO.output(18,True)
				elif value * 1.0 / 32767 >= 0.5:
					GPIO.output(17,True)
					GPIO.output(18,False)
				else:
					GPIO.output(17,False)
					GPIO.output(18,False)
			elif number == 5:
				if value * 1.0 / 32767 <= -0.5:
					GPIO.output(17,False)
					GPIO.output(18,True)
				elif value * 1.0 / 32767 >= 0.5:
					GPIO.output(17,True)
					GPIO.output(18,False)
				else:
					GPIO.output(17,False)
					GPIO.output(18,False)
