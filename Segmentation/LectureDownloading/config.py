import sys
import os

current_dir = (os.path.dirname(os.path.realpath(__file__)))
root_dir = os.path.join(current_dir,"..")
video_segmenting_dir = os.path.join(root_dir,"VideoSegmenting")
lecture_downloading_dir = os.path.join(root_dir,"LectureDownloading")
information_dir = os.path.join(root_dir,"Information")
kaltura_dir = os.path.join(root_dir,"Kaltura")

COURSE_CSV_FILE = os.path.join(information_dir, "Docs","subject.csv")   # mimght throw error
COOKIES_FILE = os.path.join(lecture_downloading_dir, "cookies.txt")                 # mimght throw error
DOWNLOADED_VIDEOS_PATH = os.path.join(information_dir,"Videos/downloaded_videos")   # ensures the vidoes are downaloded in the "downloaded_videos" folder
RECORDS_PATH = os.path.join(information_dir, "Records")