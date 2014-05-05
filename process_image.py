import pygame
import SimpleCV as scv
import SimpleCV as scv
import os
import time

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import display

############################################################################
# Global Variables
############################################################################

g_image_dir_path = os.path.join(os.getcwd(), "./images")
g_roi_dir_path = os.path.join(os.getcwd(), "./rois")
if not os.path.exists(g_roi_dir_path):
    os.mkdir(g_roi_dir_path)
g_interval_open_file = 10   # seconds

# coordinate of top-left (x, y) and the one of bottom-right (x, y)
g_roi_info = [
    # preset 1
    [
        [(171,115),(185,127)],
        [(179,127),(195,140)],
        [(185,142),(200,155)],
        [(200,145),(210,160)],
        [(207,154),(227,179)],
        [(226,140),(260,180)],
        [(230,186),(260,214)],
        [(256,204),(283,234)],
        [(280,230),(330,260)],
        [(305,270),(375,330)],
        [(380,312),(440,390)],
    ], # 0-10

    # preset 2
    [
        [(90,320), (255,452)],
        [(280,377),(593,480)],
    ], # 11-12

    # preset 3
    [
        [(97,353),(284,390)],
        [(457,388),(630,466)],
    ], # 13-14

    # preset 4
    [
        [(407,430),(570,480)],
        [(554,362),(620,404)],
        [(545,245),(640,291)]
    ], # 15-17

    # preset 5
    [
        [(348,311),(428,381)],
        [(433,265),(493,311)],
        [(484,228),(540,255)],
        [(533,203),(569,226)],
    ], # 18-21
]

g_empty_roi_info = (2, (270, 214))  # number of image, coordinate

g_number_of_preset_images = len(g_roi_info)
g_number_of_rois = sum([len(l) for l in g_roi_info])

############################################################################
# Functions
############################################################################

#Opens images, and returns an array of images
def open_images():
    files = sorted([f for f in os.listdir(g_image_dir_path) if f.startswith('2014')], reverse=True)
    try:
        paths = []
        images = []

        for i in range(1, 6):
	      ext = "p" + str(i)
	      paths.append([file for file in files if ext in file][0])

        for path in paths:
            path = os.path.join(g_image_dir_path, path)
            logger.debug("image path: %s" % (path))
            if not os.path.exists(path):
                logger.error("Error: file not exists")
                return
            else:
                #images.append(scv.Image(path))

                img = scv.Image(path)
                #img = img.convertTo(2.0, 50)
                images.append(img)
        return images
    except Exception as e:
        logger.error("The following exception was thrown, %s", e)
        return

def process(images):
    assert len(images) == g_number_of_preset_images

    for image in images:
        logger.debug(image)

    rois = []
    empty_rois = []
    len_images = len(images)

    for i in range(len_images):
        for j in range(len(g_roi_info[i])):
            #logger.debug("i: %d, j: %d" % (i, j))
            pos1 = g_roi_info[i][j][0]
            pos2 = g_roi_info[i][j][1]
            #print pos1, pos2
            #logger.debug("pos1: %s" % (pos1))
            #logger.debug("pos2: %s" % (pos2))

            width = pos2[0] - pos1[0]
            height = pos2[1] - pos1[1]
            roi = images[i].crop(pos1[0], pos1[1], width, height)
            rois.append(roi)

            x, y = g_empty_roi_info[1]
            empty_roi = images[g_empty_roi_info[0]].crop(x, y, width, height)
            empty_rois.append(empty_roi)

    assert len(rois) == g_number_of_rois

    lower_bound = 200
    threshold = 3.5

    found_empty = False

    for i in range(len(rois)):
        logger.debug("  [%02d]", i)

        roi = rois[i]
        empty_roi = empty_rois[i]

#        if i == 8:
#            roi.show()
	if i == 12:
            lower_bound = 50

        roi_edge = roi.edges(lower_bound)
        empty_edge = empty_roi.edges(lower_bound)
        diff = roi_edge - empty_edge


        path = os.path.join(g_roi_dir_path, "roi_%02d.jpg" % (i))
        logger.debug("Save roi to path: %s" % (path))
        roi.save(path)

        path = os.path.join(g_roi_dir_path, "empty_%02d.jpg" % (i))
        logger.debug("Save empty roi to path: %s" % (path))
        empty_roi.save(path)

        path = os.path.join(g_roi_dir_path, "roi-edge_%02d.jpg" % (i))
        roi_edge.save(path)

        path = os.path.join(g_roi_dir_path, "empty-edge_%02d.jpg" % (i))
        empty_edge.save(path)

        path = os.path.join(g_roi_dir_path, "diff_%02d.jpg" % (i))
        diff.save(path)

        logger.debug("  ROI / %s", roi_edge.meanColor())
        logger.debug("EMPTY / %s", empty_edge.meanColor())
        logger.debug(" DIFF / %s", diff.meanColor())

        b, g, r = diff.meanColor()
        if r > threshold and g > threshold and b > threshold:
            #logger.debug("Occupied")
            pass
        else:
            #logger.debug("Empty")
            logger.debug("Empty spot found on [%02d]" % (i))
            found_empty = True
            break

    if found_empty:
        logger.debug("Send signal 1")
        display.signaltoDisplay(1)
    else:
        logger.debug("Send signal 0")
        display.signaltoDisplay(1)

def run():
    while True:
        logger.debug("Call open_images()")
        images = open_images()
        if images:
            logger.debug("Call process()")
            process(images)
        logger.debug("Sleep %d seconds between loop" % (g_interval_open_file))
        time.sleep(g_interval_open_file)

############################################################################
#
############################################################################

if __name__ == "__main__":
    run()
