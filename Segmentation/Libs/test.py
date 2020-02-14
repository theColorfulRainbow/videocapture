from Logger import logger
import logging
import os 
from VideoSegmenting.Segmentor import Segmentor
from LectureDownloading.download_all_lectures import *

logger.setLevel(logging.DEBUG)
logger.debug("Hello")
logger.debug(os.path.dirname(os.path.realpath(__file__)))