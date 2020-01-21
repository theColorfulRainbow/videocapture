from Segmentor import Segmentor
import os
import sys
import time
from Subject import Subject, Subject_List
import logging
import Logger
from Video import Video

# gets path to scripts for downloading videos
# lecture_downloading_path = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir),"LectureDownloading")
# allows us to import download scripts
# sys.path.insert(1, lecture_downloading_path)

from download_all_lectures import begin as download_lecture

logger = logging.getLogger("Logger")

# print(lecture_downloading_path)
# GOES BACK TWO times ("+ os.sep + os.pardir" x 2) and goes into Videos folder
VIDEO_DIRECTORY = os.path.join(os.getcwd(), "Videos")
COURSE_CSV_FILE = os.path.join(os.getcwd(), "Docs/subject.csv")

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
    # videos = download_lectures()
    # print('videos=\n{}'.format(videos))
    # testing the qr video we made
    videos = [Video("SCEE08007","2017-2018","2019-08-10T12:00Z","secondary.mp4","/afs/inf.ed.ac.uk/user/s16/s1628465/Desktop/my_git/TestingEnvironment/segment/downloaded_videos/2019-2020/SCEE08007/2020-01-17T11.10.00.000Z/secondary.mp4")]
    logger.info("Lectures Downloaded!")
    # get all the subjects
    subjects = Subject_List(COURSE_CSV_FILE)

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
