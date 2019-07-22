import charsing_controller as cs
import joystick_controller as js
import motor_driver as md

class TotalController:
    def __init__(self):
        # 0:待机模式 1:遥控 2:追踪
        self._state = 0
        # 0:静止 1:前进 2:后退 3:左转 4:右转
        self._action = 0
        # 0:有障碍物 1:无障碍物
        self._lidar = 0
        # 打开手柄


    def descision(self):
        if(self._state == 0):
            md.stop()


