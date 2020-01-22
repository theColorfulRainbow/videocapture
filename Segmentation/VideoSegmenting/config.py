import sys
import os
current_dir = (os.path.dirname(os.path.realpath(__file__)))
root_dir = os.path.join(current_dir,"..")
video_segmenting_dir = os.path.join(root_dir,"VideoSegmenting")
lecture_downloading_dir = os.path.join(root_dir,"LectureDownloading")
information_dir = os.path.join(root_dir,"Information")
kaltura_dir = os.path.join(root_dir,"Kaltura")

VIDEO_DIRECTORY = os.path.join(information_dir,"Videos/segmented_videos")
COURSE_CSV_FILE = os.path.join(information_dir, "Docs/subject.csv")