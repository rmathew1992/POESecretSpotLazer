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

#g_approach_num = 'A_1'
g_approach_num = 'B_1'
# A-1: mean color difference
# B-1: edge detection

g_input_from_user = False

############################################################################
# Functions
############################################################################

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

def A_1(parking_areas_full, parking_areas_empty):
    #####
    # First approach: mean color difference
    # - Pros: easy
    # - Cons: need previously stored standard data based on time
    #         inaccurate? maybe?
    #####

    mean_colors_full = []
    for parking_area in parking_areas_full:
        mean_colors_full.append(parking_area.meanColor())

    mean_colors_empty = []
    for parking_area in parking_areas_empty:
        mean_colors_empty.append(parking_area.meanColor())


    # Suppose threshold to detect difference in these pictures is 115
    # Since empty space is almost grey, we can set same threshold to R,G and B.
    threshold = 115

    print "== Full parking lot"
    for i in range(g_parking_area_num):
        b, g, r = mean_colors_full[i]
        if r > threshold and g > threshold and b > threshold:
            print "Parking Lot %d --> Empty" % (i)
        else:
            print "Parking Lot %d --> Occupied" % (i)

    print "== Empty parking lot"
    for i in range(g_parking_area_num):
        b, g, r = mean_colors_empty[i]
        if r > threshold and g > threshold and b > threshold:
            print "Parking Lot %d --> Empty" % (i)
        else:
            print "Parking Lot %d --> Occupied" % (i)

    return

"""
0: [0.000000, 0.000000, 0.000000]
1: [1.523377, 1.523377, 1.523377]
2: [23.485185, 23.485185, 23.485185]
3: [0.000000, 0.000000, 0.000000]
4: [0.000000, 0.000000, 0.000000]
5: [0.000000, 0.000000, 0.000000]
"""
def B_1(parking_areas_full, parking_areas_empty):
    #####
    # Second approach: edge detection + difference between edges + mean color difference
    # - Pros:
    # - Cons:
    #####

    #parking_areas_full[2].edges(300).show()
    #parking_areas_empty[2].edges(300).show()

    lower_bound = 300
    threshold = 5.0

    for i in range(g_parking_area_num):
        diff = parking_areas_full[i].edges(lower_bound) - parking_areas_empty[i].edges(lower_bound)
        b, g, r = diff.meanColor()
        #print "%d: [%f, %f, %f]" % (i, r, g, b)
        if r > threshold and g > threshold and b > threshold:
            print "Parking Lot %d --> Empty" % (i)
        else:
            print "Parking Lot %d --> Occupied" % (i)


def get_ROI_from_image(image_path):
    parking_areas = []

    img = scv.Image(image_path)
    for i in range(g_parking_area_num):
        pos = g_parking_area_pos[i]
        size = g_parking_area_size[i]
        parking_areas.append(img.crop(pos[0], pos[1], size[0], size[1]))

    return parking_areas

def process(file_full, file_empty, roi):
    if not os.path.exists(file_full) or not os.path.exists(file_empty):
        print "Error: file not exists"
        return

    # get ROIs
    parking_areas_full = get_ROI_from_image(file_full)
    parking_areas_empty = get_ROI_from_image(file_empty)

    if g_approach_num == 'A_1':
        A_1(parking_areas_full, parking_areas_empty)
    elif g_approach_num == 'B_1':
        B_1(parking_areas_full, parking_areas_empty)

if __name__ == "__main__":
    while True:
        if g_input_from_user:
            file_path_1 = raw_input("# Input file path of full parking lot (exit: x): ")
            file_path_2 = raw_input("# Input file path of empty parking lot (exit: x): ")
            if file_path_1 == "x" or file_path_2 == "x":
                break
        else:
            inp = raw_input("Input any (exit: x): ")
            if inp == "x":
                break
            file_path_1 = "./parkinglot_full.png"
            file_path_2 = "./parkinglot_empty_2.png"
        n = None
    ## for testing
#        n = int(raw_input("# ROI Num: "))
    ##
        process(file_path_1, file_path_2, n)