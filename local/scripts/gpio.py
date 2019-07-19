import RPi.GPIO as GPIO   #先要导入模块

GPIO.setwarnings(False)

##BCM 对应  17 18 27 22
GPIO.setmode(GPIO.BCM)     #选择 GPIO numbers 编号系统

GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
#GPIO.setup(27,GPIO.OUT)
#GPIO.setup(22,GPIO.OUT)

GPIO.output(17,True)
GPIO.output(18,True)
