import RPi.GPIO as GPIO   #先要导入模块

# fl fr bl br
bcm_table = ((4, 25), (17, 18), (23, 24), (22, 27))


def motor_init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in range(4):
        for j in range(2):
            GPIO.setup(bcm_table[i][j], GPIO.OUT)


def motor_stop(bcm_tuples):
    GPIO.output(bcm_tuples[0], False)
    GPIO.output(bcm_tuples[1], False)


def motor_forward(bcm_tuples):
    GPIO.output(bcm_tuples[0],True)
    GPIO.output(bcm_tuples[1], False)


def motor_backward(bcm_tuples):
    GPIO.output(bcm_tuples[1], True)
    GPIO.output(bcm_tuples[0], False)


def turn_left():
    motor_backward(bcm_table[0])
    motor_backward(bcm_table[2])
    motor_forward(bcm_table[1])
    motor_forward(bcm_table[3])


def turn_right():
    motor_forward(bcm_table[0])
    motor_forward(bcm_table[2])
    motor_backward(bcm_table[1])
    motor_backward(bcm_table[3])


def go_forward():
    motor_forward(bcm_table[0])
    motor_forward(bcm_table[2])
    motor_forward(bcm_table[1])
    motor_forward(bcm_table[3])


def go_backward():
    motor_backward(bcm_table[0])
    motor_backward(bcm_table[2])
    motor_backward(bcm_table[1])
    motor_backward(bcm_table[3])


def stop():
    for i in range(4):
        motor_stop(bcm_table[i])