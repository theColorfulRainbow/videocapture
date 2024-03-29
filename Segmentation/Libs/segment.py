import sys
sys.path.append('.')

import os
import time
import logging
from pathlib import Path

from VideoSegmenting.Segmentor import Segmentor
from Video import Video
from LectureDownloading.download_all_lectures import begin as download_lecture
from config import VIDEO_DIRECTORY, COURSE_CSV_FILE, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT
from VideoSegmenting.Sub_Clip import combine_frame_stamps, frame_number_to_time, create_subClips

logger = logging.getLogger("Logger")

# GOES BACK TWO times ("+ os.sep + os.pardir" x 2) and goes into Videos folder
current_dir = os.path.dirname(os.path.realpath(__file__))

def segment(video, threshold_frame_continuous, threshold_frame_timeout):
    logger.info("Segmenting Video: {}, Threshold Frame Continuous: {}, Threshold Frame Timeout: {}".format(video.code,threshold_frame_continuous, threshold_frame_timeout))
    # intialise segmentor
    my_Segmentor = Segmentor(video, threshold_frame_continuous, threshold_frame_timeout)
    # time_array should also be set in the Video object itself
    frame_stamps = my_Segmentor.start()
    return frame_stamps

# downloads all the lectures
def download_lectures():
    logger.info("Downloading Lectures...")
    return download_lecture()

# uploads all the segmented videos and performs safety checks
def upload_video(video_dir):
    return

def start(duo_videos,threshold_frame_continuous, threshold_frame_timeout):
    # check if videos empty
    if (len(duo_videos) == 0):
        logger.info("No new lectures Downloaded, exiting!")
        exit()

    # segment each video
    frame_stamps = []
    for videos in duo_videos:
        frame_stamps = []
        for video in videos:
            # check if primary video is null
            if (video == None):
                logger.debug("Video is None... ignoring".format())    
            else:
                logger.info("\nSegmenting Video {}".format(video))
                logger.debug("In for loop, about to segment {}".format(video.code))
                logger.info("Video has a frame rate of ~{} and total number of frame ~{}".format(video.get_frame_rate(), video.get_total_frames()))
                # make the folder if it doesnt exist
                if os.path.isdir(video.get_destination_directory()) == False:
                    # creates parents directory if they dont exist, better than os.mkdir
                    Path(video.get_destination_directory()).mkdir(parents=True, exist_ok=True)

                logger.debug("Video: {}".format(video))
                # segment the video
                frame_stamp = segment(video, threshold_frame_continuous, threshold_frame_timeout )
                frame_stamps.append(frame_stamp)
                logger.debug("Appending Frame stamp {}".format(frame_stamps))
        
        # check that both videos have same number of frames and frame_rate
        if (videos[0] != None):
            # deal with time_stamps
            logger.info("Raw Frame Stamp Dictionaries: {}".format(frame_stamps))
            combined_frame_stamp = combine_frame_stamps(frame_stamps)
            logger.info("Video {}, Frame rate: {}, Total Number of Frames: {}".format(videos[0], videos[0].number_of_frames, videos[0].fps))
            time_array = frame_number_to_time(combined_frame_stamp, videos[0].number_of_frames, videos[0].fps)

            logger.info("Time Array: {}".format(time_array))
            # create the sub clips
            for video in videos:
                logger.info("Creating Sub Clips...")
                if (video != None):
                    # sub_directory = os.path.join(segmented_video_path,Video.date_time,Video.video_type)
                    create_subClips(video.get_video_path(), video.get_destination_directory(), time_array, video.get_video_name())
            #return time_array
        # upload the segmented video to media hopper create
        # upload_video(segmented_video_path)

def segment_all_lectures():
    #download and get all the videos to segment
    duo_videos = download_lectures()

    # testing the qr video we made
    test_video_primary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4","/afs/inf.ed.ac.uk/user/s16/s1645821/Desktop/segmentation_git/Segmentation/UnitTests/TestVideos/scenario_4_2_QR_till_end/video_primary.mp4")
    test_video_secondary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","primary.mp4","/afs/inf.ed.ac.uk/user/s16/s1645821/Desktop/segmentation_git/Segmentation/UnitTests/TestVideos/scenario_4_2_QR_till_end/video_secondary.mp4")
    #duo_videos = [[test_video_primary, test_video_secondary]]
    logger.info("Lectures Downloaded!")
    threshold_frame_continuous = THRESHOLD_FRAME_CONTINUOUS
    threshold_frame_timeout = THRESHOLD_FRAME_TIMEOUT
    start(duo_videos, threshold_frame_continuous,threshold_frame_timeout)

# the main operation
def main():
    logger.setLevel(logging.INFO)
    logger.info(30*"-" + "\nBeginning Segmentation")
    segment_all_lectures()

if (__name__ == "__main__"):
    main()
