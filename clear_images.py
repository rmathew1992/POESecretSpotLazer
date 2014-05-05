import time
import datetime
import os

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

############################################################################
# Global Variables
############################################################################

g_image_dir_path = os.path.join(os.getcwd(), "./images")
files = sorted([f for f in os.listdir(g_image_dir_path) if f.startswith('2014')], reverse=True)
current_day = datetime.datetime.today().day 
def clearOld():
	for file in files:
		day = int(file[8:10])
		if current_day != day:
			os.remove(os.path.join(g_image_dir_path, file))
	return

def run():
	clearOld()
	return

run()