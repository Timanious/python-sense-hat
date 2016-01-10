#!/usr/bin/python
import sys
from sense_hat import SenseHat

# To get good results with the magnetometer you must first calibrate it using
# the program in RTIMULib/Linux/RTIMULibCal
# The calibration program will produce the file RTIMULib.ini
# Copy it into the same folder as your Python code

led_loop = [
            [3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2],
            [4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2, 3],
            [11,12,13,14,22,30,38,46,54,53,52,51,50,49,41,33,25,17,9,10],
            [12,13,14,22,30,38,46,54,53,52,51,50,49,41,33,25,17,9,10,11],
            [19,20,21,29,37,45,44,43,42,34,26,18],
            [20,21,29,37,45,44,43,42,34,26,18,19],
            [27,28,36,35],
            [28,36,35,27],
            [36,35,27,28],
            [35,27,28,36],
            [44,43,42,34,26,18,19,20,21,29,37,45],
            [43,42,34,26,18,19,20,21,29,37,45,44],
            [52,51,50,49,41,33,25,17,9,10,11,12,13,14,22,30,38,46,54,53],
            [51,50,49,41,33,25,17,9,10,11,12,13,14,22,30,38,46,54,53,52],
            [60, 59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61],
            [59, 58, 57, 56, 48, 40, 32, 24, 16, 8, 0, 1, 2, 3, 4, 5, 6, 7, 15, 23, 31, 39, 47, 55, 63, 62, 61, 60],
           ]

sense = SenseHat()
sense.set_rotation(0)
sense.clear()

prev_x=[]
prev_y=[]
led_degree_ratio=[]

for i in range(0,len(led_loop)):
    prev_x.append( 0 )
    prev_y.append( 0 )
    led_degree_ratio.append( (len(led_loop[i])+1)/360.0 )

while True:
    dir = sense.get_compass()
    dir_inverted = 90 - dir  # So LED appears to follow North

    led_index = []
    offset = []
    x = []
    y = []

    for i in range(0,len(led_loop)):
        led_index.append( int(led_degree_ratio[i] * dir_inverted) )
        offset.append( led_loop[i][led_index[i]] )
        x.append( offset[i] %  8 ) # column
        y.append( offset[i] // 8 ) # row

        if x[i] != prev_x[i] or y[i] != prev_y[i]:
            sense.set_pixel(prev_x[i], prev_y[i], 0, 0, 0)

        if i < 8:
            sense.set_pixel(x[i], y[i], 255, 0, 0)
        else:
            sense.set_pixel(x[i], y[i], 0, 0, 255)
        prev_x[i] = x[i]
        prev_y[i] = y[i]
