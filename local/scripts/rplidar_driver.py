#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/dev/ttyUSB0'
DMAX = 4000
IMIN = 0
IMAX = 50

def run():
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    for measurment in lidar.iter_measurments():
        line = '\t'.join(str(v) for v in measurment)
        print(line)
    lidar.stop()
    lidar.disconnect()


run()