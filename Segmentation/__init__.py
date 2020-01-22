from config import *

sys.path.append(root_dir)
sys.path.append(video_segmenting_dir)
sys.path.append(lecture_downloading_dir)
sys.path.append(information_dir)
sys.path.append(kaltura_dir)

from Logger import logger
import logging
from Subject import Subject, Subject_List
from Video import Video
from VideoSegmenting.Segmentor import Segmentor

# DEBUG
# logger.setLevel(logging.DEBUG)
# logger.debug("Hello init Master")
# logger.debug('{}\n{}'.format(VIDEO_DIRECTORY,COURSE_CSV_FILE))