# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 13:57:25 2014

@author: sim
"""

import SimpleCV as scv
import time
import os, sys

############################################################################
# Global Variables
############################################################################

g_parking_area_num = 6

# pair of x and y
g_parking_area_pos = [
    [30, 150],
    [200, 140],
    [350, 135],
    [500, 135],
    [640, 135],
    [780, 127],
]

# pair of width and height
g_parking_area_size = [
    [145, 60],
    [140, 55],
    [135, 60],
    [125, 75],
    [115, 90],
    [140, 60],
]

############################################################################
# Functions
############################################################################

def process(file_path, roi):
    if not os.path.exists(file_path):
        print "Error: file not exists"
        return

    img = scv.Image(file_path)
    #img.show()

    # Crop ROI
    parking_areas = []

    for i in range(g_parking_area_num):
        pos = g_parking_area_pos[i]
        size = g_parking_area_size[i]
        parking_areas.append(img.crop(pos[0], pos[1], size[0], size[1]))

    if roi != None:
        parking_areas[roi].show()

    """
    # Full
(84.41275862068966, 79.07264367816092, 82.55540229885057)
(71.57948051948053, 68.4587012987013, 71.66545454545455)
(108.60111111111111, 104.85925925925926, 113.59135802469136)
(94.56906666666667, 89.88106666666667, 94.90229333333333)
(100.20695652173913, 94.34144927536232, 103.79690821256038)
(80.70869047619047, 70.23428571428572, 74.88821428571428)
    # Empty (2)
(83.41275862068966, 78.07264367816092, 81.55540229885057)
(70.20181818181818, 66.8603896103896, 69.25051948051949)
(126.66185185185185, 123.67185185185186, 129.15814814814814)
(93.56906666666667, 88.88138666666667, 93.90229333333333)
(99.20695652173913, 93.34144927536232, 102.79690821256038)
(79.70869047619047, 69.23428571428572, 73.88821428571428)
    """
    #####
    # First approach: mean color difference
    # - Pros: easy
    # - Cons: need previously stored standard data based on time
    #####

    mean_colors = []
    for parking_area in parking_areas:
        mean_colors.append(parking_area.meanColor())

    # Suppose threshold to detect difference in these pictures is 115
    # Since empty space is almost grey, we can set same threshold to R,G and B.
    threshold = 115

    for i in range(g_parking_area_num):
        b, g, r = mean_colors[i]
        if r > threshold and g > threshold and b > threshold:
            print "Parking Lot %d --> Empty" % (i)
        else:
            print "Parking Lot %d --> Occupied" % (i)

"""
    parking_area = img.crop(470, 200, 200, 200)
    yellow_car = parking_area.colorDistance(scv.Color.YELLOW)
    only_car = parking_area - yellow_car
    b, g, r = only_car.meanColor() # caution, BGR!!

    print "Red: %d / Green: %d / Blue: %d" % (r, g, b)
    if r > 15 and g > 10:
        print "There is a car."
    else:
        print "There is no car."
"""

if __name__ == "__main__":
    while True:
        file_path = raw_input("# Input image file path (exit: x): ")
        if file_path == "x":
            break
        n = None
        ## for testing
#        n = int(raw_input("# ROI Num: "))
        ##
        process(file_path, n)