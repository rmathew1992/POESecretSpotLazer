# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 13:57:25 2014

@author: sim
"""

import SimpleCV as scv
import time
import os

def process(file_path):
    if not os.path.exists(file_path):
        print "Error: file not exists"
        return

    img = scv.Image(file_path)
    parking_area = img.crop(470, 200, 200, 200)
    yellow_car = parking_area.colorDistance(scv.Color.YELLOW)
    only_car = parking_area - yellow_car
    b, g, r = only_car.meanColor() # caution, BGR!!
    # I think there is an an error in
    #   http://tutorial.simplecv.org/en/latest/examples/parking.html
    #  Checking R and B should be changed to checking R and G.

    print "Red: %d / Green: %d / Blue: %d" % (r, g, b)
    if r > 15 and g > 10:
        print "There is a car."
    else:
        print "There is no car."

if __name__ == "__main__":
    while True:
        file_path = raw_input("# Input image file path (exit: x): ")
        if file_path == "x":
            break
        process(file_path)