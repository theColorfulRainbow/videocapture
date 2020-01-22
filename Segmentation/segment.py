from VideoSegmenting.Segmentor import Segmentor
import os
import sys
import time
import logging
from Video import Video
from download_all_lectures import begin as download_lecture
from config import VIDEO_DIRECTORY, COURSE_CSV_FILE

logger = logging.getLogger("Logger")

# GOES BACK TWO times ("+ os.sep + os.pardir" x 2) and goes into Videos folder
current_dir = os.path.dirname(os.path.realpath(__file__))

def segment(video_path, segmented_video_path, subject):
    logger.debug("Segmenting with video_path: {}, segmented video_path: {}, subject: {}".format(video_path, segmented_video_path, subject.code))
    # intialise segmentor
    my_Segmentor = Segmentor(video_path,segmented_video_path, subject)
    my_Segmentor.start()

# downloads all the lectures
def download_lectures():
    logger.info("Downloading Lectures...")
    return download_lecture()

# uploads all the segmented videos and performs safety checks
def upload_video(video_dir):
    return

# the main operation
def main():
    logger.setLevel(logging.DEBUG)
    # download and get all the videos to segment
    videos = download_lectures()

    # testing the qr video we made
    # videos = [Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4","/afs/inf.ed.ac.uk/user/s16/s1645821/lecture_recording/MasterEnvironemnt/Information/Videos/test_videos/James_Hopgood_Lecture_Trim.mp4")]
    logger.info("Lectures Downloaded!")

    # check if videos empty
    if (len(videos) == 0):
        logger.info("No new lectures Downloaded, exiting!")
        exit()

    # segment each video
    for video in videos:
        logger.info("Segmenting Video {}".format(video))
        logger.debug("In for loop, about to segment {}".format(video.code))
        segmented_video_path = os.path.join(VIDEO_DIRECTORY,video.code)
        # make the folder if it doesnt exist
        if os.path.isdir(segmented_video_path) == False:
            os.mkdir(segmented_video_path)

        # subject = subjects.get_subject_via_code(course_code)
        logger.debug("Video: {}".format(video))
        # segment the video
        segment(video.get_video_path(), segmented_video_path, video)
        # upload the segmented video to media hopper create
        upload_video(segmented_video_path)

if (__name__ == "__main__"):
    main()
