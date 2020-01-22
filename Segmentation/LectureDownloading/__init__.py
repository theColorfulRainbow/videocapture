import sys
import os

from config import *

sys.path.append(root_dir)
sys.path.append(video_segmenting_dir)
sys.path.append(lecture_downloading_dir)
sys.path.append(information_dir)
sys.path.append(kaltura_dir)


from Video import Video
from Subject import Subject, Subject_List
