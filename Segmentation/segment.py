from VideoSegmenting.Segmentor import Segmentor
import os
import sys
import time
import logging
from Video import Video
from download_all_lectures import begin as download_lecture
from config import VIDEO_DIRECTORY, COURSE_CSV_FILE
from Sub_Clip import combine_frame_stamps, frame_number_to_time, create_subClips

logger = logging.getLogger("Logger")

# GOES BACK TWO times ("+ os.sep + os.pardir" x 2) and goes into Videos folder
current_dir = os.path.dirname(os.path.realpath(__file__))

def segment(video_path, segmented_video_path, subject):
    logger.debug("Segmenting with video_path: {}, segmented video_path: {}, subject: {}".format(video_path, segmented_video_path, subject.code))
    # intialise segmentor
    my_Segmentor = Segmentor(video_path,segmented_video_path, subject)
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

# the main operation
def main():
    logger.setLevel(logging.DEBUG)
    # download and get all the videos to segment
    # duo_videos = download_lectures()

    # testing the qr video we made
    test_video = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4","/afs/inf.ed.ac.uk/user/s16/s1645821/Desktop/segmentation_git/Segmentation/Information/Videos/test_videos/test_QR_13s.mp4")
    duo_videos = [ [test_video, None],[None,None] ]
    logger.info("Lectures Downloaded!")

    # check if videos empty
    if (len(duo_videos) == 0):
        logger.info("No new lectures Downloaded, exiting!")
        exit()

    # segment each video
    for videos in duo_videos:
        frame_stamps = []
        for video in videos:
            # check if primary video is null
            if (video == None):
                logger.debug("Video is None... ignoring".format())    
            else:
                logger.info("Segmenting Videos {}".format(video))
                logger.debug("In for loop, about to segment {}".format(video.code))
                segmented_video_path = os.path.join(VIDEO_DIRECTORY,video.code)
                # make the folder if it doesnt exist
                if os.path.isdir(segmented_video_path) == False:
                    os.mkdir(segmented_video_path)

                logger.debug("Video: {}".format(video))
                # segment the video
                frame_stamp = segment(video.get_video_path(), segmented_video_path, video)
                frame_stamps.append(frame_stamp)
                logger.debug("Appending Frame stamp {}".format(frame_stamps))
        # deal with time_stamps
        combined_frame_stamp = combine_frame_stamps(frame_stamps)
        # check that both videos have same number of frames and frame_rate
        if (videos[0] != None):
            time_array = frame_number_to_time(combined_frame_stamp, videos[0].number_of_frames, videos[0].fps)
            logger.info("Time Array: {}".format(time_array))
            # create the sub clips
            for video in videos:
                logger.info("Creating Sub Clips...")
                if (video != None):
                    create_subClips(video.get_video_path(), segmented_video_path, time_array, video.get_video_name())
        # upload the segmented video to media hopper create
        # upload_video(segmented_video_path)

if (__name__ == "__main__"):
    main()
