import RPi.GPIO as GPIO   #先要导入模块

GPIO.setwarnings(False)

##BCM 对应  17 18 27 22
GPIO.setmode(GPIO.BCM)     #选择 GPIO numbers 编号系统

GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
## 17 True 18 False fr forward
## 23 True 24 False bl forward
## 4 True 25 False fl forward wrong
## 22 True 27 False br forward
GPIO.output(17,True)
GPIO.output(18,False)
GPIO.output(23,True)
GPIO.output(24,False)
GPIO.output(4,True)
GPIO.output(25,False)
GPIO.output(22,True)
GPIO.output(27,False)
