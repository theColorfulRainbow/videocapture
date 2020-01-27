from VideoSegmenting.Segmentor import Segmentor
import os
import sys
import time
import logging
from Video import Video
from download_all_lectures import begin as download_lecture
from config import VIDEO_DIRECTORY, COURSE_CSV_FILE, THRESHOLD_FRAME
from Sub_Clip import combine_frame_stamps, frame_number_to_time, create_subClips
from pathlib import Path


logger = logging.getLogger("Logger")

# GOES BACK TWO times ("+ os.sep + os.pardir" x 2) and goes into Videos folder
current_dir = os.path.dirname(os.path.realpath(__file__))

def segment(video_path, segmented_video_path, subject, threshold_frame):
    logger.debug("Segmenting with video_path: {}, segmented video_path: {}, subject: {}, threshold_frame".format(video_path, segmented_video_path, subject.code,threshold_frame))
    # intialise segmentor
    my_Segmentor = Segmentor(video_path,segmented_video_path, subject, threshold_frame=threshold_frame)
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

def start(duo_videos,threshold_frame=THRESHOLD_FRAME):
    # check if videos empty
    if (len(duo_videos) == 0):
        logger.info("No new lectures Downloaded, exiting!")
        exit()

    # segment each video
    frame_stamps = []
    for videos in duo_videos:
        for video in videos:
            # check if primary video is null
            if (video == None):
                logger.debug("Video is None... ignoring".format())    
            else:
                logger.info("\nSegmenting Video {}".format(video))
                logger.debug("In for loop, about to segment {}".format(video.code))
                # make the folder if it doesnt exist
                if os.path.isdir(video.get_destination_directory()) == False:
                    # creates parents directory if they dont exist, better than os.mkdir
                    Path(video.get_destination_directory()).mkdir(parents=True, exist_ok=True)

                logger.debug("Video: {}".format(video))
                # segment the video
                frame_stamp = segment(video.get_video_path(), video.get_destination_directory(), video, threshold_frame)
                frame_stamps.append(frame_stamp)
                logger.debug("Appending Frame stamp {}".format(frame_stamps))
        
        # check that both videos have same number of frames and frame_rate
        if (videos[0] != None):
            # deal with time_stamps
            logger.info("Raw Frame Stamp Dictionaries: {}".format(frame_stamps))
            combined_frame_stamp = combine_frame_stamps(frame_stamps)
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

# the main operation
def main():
    logger.setLevel(logging.DEBUG)
    logger.info(30*"-" + "\nBeginning Segmentation")
    # download and get all the videos to segment
    duo_videos = download_lectures()

    # testing the qr video we made
    test_video = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4","/afs/inf.ed.ac.uk/user/s16/s1645821/Desktop/segmentation_git/Segmentation/Information/Videos/test_videos/James_Hopgood_Lecture_Trim.mp4")
    #duo_videos = [ [test_video, None],[None,None] ]
    logger.info("Lectures Downloaded!")
    threshold_frame = THRESHOLD_FRAME
    start(duo_videos, threshold_frame=THRESHOLD_FRAME)

if (__name__ == "__main__"):
    main()
