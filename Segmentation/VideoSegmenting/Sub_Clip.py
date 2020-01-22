# This file will deal with breaking
# up the video into frames and saving those
# frames as png files

## TESTED and Working 20/12/18

import os
import math
from moviepy.editor import *
import logging
# import MasterEnvironemnt.Logger 
logger = logging.getLogger("Logger")

# code taken from https://stackoverflow.com/questions/43148590/extract-images-using-opencv-and-python-or-moviepy
# assume times array has the end time for the clip since we will not have
# an identifier in the last slide
def create_subClips(movie,destination_directory,times_array,course_name):
    # load information about clip to variables
    clip = VideoFileClip(movie)
    # check that last element in times array is within video duration
    if(times_array[-1]>clip.duration):
        times_array[-1] = int(math.floor(clip.duration))
    print('clip_duration={}\ntimes_array={}'.format(clip.duration,times_array))
    # define variable for when to start the clip to where to end it
    last_time = 0
    # create sub clips array
    sub_clip_array = []
    # create sub clips and save them to the sub_clip_array
    for time in times_array:
        sub_clip = clip.subclip(last_time, time)
        sub_clip_array.append(sub_clip)
        last_time = time
    # save the sub clips to a directory
    for i in range(len(sub_clip_array)):
        topic_name = "Topic_{}_{}.mp4".format(i,course_name)
        name = os.path.join(destination_directory,topic_name)
        sub_clip_array[i].write_videofile(name)


def combine_frame_stamps(topic_frame_dicts):
    finale_frame_stamp = {}
    for dictionary in topic_frame_dicts:
        for key, value in dictionary.items():
            # check if there is already an entry for the given topic number
            if (key in finale_frame_stamp):
                # check if the frame number is greate than the stored frame number
                stored_frame = finale_frame_stamp[key]
                if (value < stored_frame):
                    finale_frame_stamp[key] = stored_frame
                    logger.debug("Updated Final Time Stamp Dictionary from ({}) vs ({})".format(stored_frame,value))
            else:
                finale_frame_stamp[key] = value
                logger.debug("Added ({} : {}) to Final Time Stamp Dictionary".format(key,value))

    # ordered_dict = sorted(finale_frame_stamp, key=finale_frame_stamp.get, reverse=False)
    logger.info("Final Time Stamp Dictionary: {}".format(finale_frame_stamp))
    # convert each frame nnumber to a time
    return finale_frame_stamp
            
# most updated!!
def frame_number_to_time(dictionary, frame_number, frame_rate):
    logger.debug("Getting frame number to time...")
    times_array = list()
    for topic in dictionary:
        time = math.floor(_convert_frame_num_to_time( frame_number=dictionary[topic], frame_rate=frame_rate))
        times_array.append(time)

    # check if the last fraame is in times array, if not then add it
    last_frame_time = math.floor(_convert_frame_num_to_time( frame_number=frame_number, frame_rate=frame_rate))
    # logger.debug('dictionary = {}\ntimes_array = {}\nlast frame number = {} last_frame_time={}'.format(dictionary, times_array, frame_number, last_frame_time))

    if not(last_frame_time in times_array):
        times_array.append(last_frame_time)

    # logger.debug('times_array = {}\nlast_frame_time={}'.format(times_array,last_frame_time))
    return times_array      

# convert a frame number to second
def _convert_frame_num_to_time(frame_number, frame_rate):
    logger.debug("Converting frame number to time...")
    return (frame_number/frame_rate)