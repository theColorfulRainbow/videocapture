import sys
import os

# MAIN DIRECTORIES
unitTest_dir = (os.path.dirname(os.path.realpath(__file__)))
root_dir    = (os.path.join(unitTest_dir,".."))
video_segmenting_dir = os.path.join(root_dir,"VideoSegmenting")
lecture_downloading_dir = os.path.join(root_dir,"LectureDownloading")
information_dir = os.path.join(root_dir,"Information")
kaltura_dir = os.path.join(root_dir,"Kaltura")
log_dir = os.path.join(information_dir,"LogFiles")

# Test Videos Directories
test_videos_dir = os.path.join(unitTest_dir,"TestVideos")
test_videos_scenario_perfect_dir = os.path.join(test_videos_dir,"scenario_perfect")
test_videos_scenario_secondary_empty = os.path.join(test_videos_dir,"scenario_secondary_empty")
test_videos_scenario_topics_behind = os.path.join(test_videos_dir,"scenario_topics_behind")
scenario_4_2_QR_till_end = os.path.join(test_videos_dir,"scenario_4_2_QR_till_end")

# INFORMATION FILES
VIDEO_DIRECTORY = os.path.join(information_dir,"Videos/segmented_videos")
COURSE_CSV_FILE = os.path.join(information_dir, "Docs/subject.csv")
THRESHOLD_FRAME_CONTINUOUS = 120 #~4s
THRESHOLD_FRAME_TIMEOUT = 300 #~10S