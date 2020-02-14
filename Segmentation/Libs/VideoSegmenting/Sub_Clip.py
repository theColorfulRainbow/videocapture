# This file will deal with breaking
# up the video into frames and saving those
# frames as png files

## TESTED and Working 20/12/18

import os
import math
from moviepy.editor import *
import logging
from config import VIDEO_DIRECTORY
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
    logger.info('clip_duration: {}\ntimes_array: {}'.format(clip.duration,times_array))
    # define variable for when to start the clip to where to end it
    last_time = 0
    # create sub clips array
    sub_clip_array = []
    # create sub clips and save them to the sub_clip_array
    for time in times_array:
        if (not (last_time <= time)):
            exception_msg = "Trying to Segent video where this time: {} is less than previous segmented time: {}".format(time, last_time)
            logger.exception(exception_msg)
            raise Exception(exception_msg)
        else:    
            logger.debug("Segmenting Video from {} -> {}".format(last_time, time))
            sub_clip = clip.subclip(last_time, time)
            sub_clip_array.append(sub_clip)
            last_time = time

    # save the sub clips to a directory
    for i in range(len(sub_clip_array)):
        logger.info("Saving segmented videos")
        # check if sub-folder for date-time exists
        if (not os.path.isdir(destination_directory)):
            logger.info("Creating Directory: {}".format(destination_directory))
            os.mkdir(destination_directory)

        topic_name = "{}_topic_{}.mp4".format(course_name, i+1)
        name = os.path.join(destination_directory,topic_name)
        sub_clip_array[i].write_videofile(name)
        logger.info("Saving Video: {}".format(name))


def combine_frame_stamps(topic_frame_dicts):
    finale_frame_stamp = {}
    for dictionary in topic_frame_dicts:
        for key, value in dictionary.items():
            # check if there is already an entry for the given topic number
            if (key in finale_frame_stamp):
                # check if the frame number is greater than the stored frame number
                stored_frame = finale_frame_stamp[key]
                if (value > stored_frame):
                    finale_frame_stamp[key] = value
                    logger.debug("Updated Final Time Stamp Dictionary from ({}) vs ({})".format(stored_frame,value))
            else:
                finale_frame_stamp[key] = value
                logger.debug("Added ({} : {}) to Final Time Stamp Dictionary".format(key,value))

    # ordered_dict = sorted(finale_frame_stamp, key=finale_frame_stamp.get, reverse=False)
    logger.info("Final Time Stamp Dictionary: {}".format(finale_frame_stamp))

    valid_frame_stamp_dictionary = create_valid_dictionary(finale_frame_stamp)

    # convert each frame nnumber to a time
    return valid_frame_stamp_dictionary

# creates a dictionary where the topic number with lowest frame count is '1st' and all others are in ascending order 
def create_valid_dictionary(dictionary):
    logger.debug("Creating valid dictionary")
    try:
        lowest_topic_num = min(dictionary, key=dictionary.get)
        lowest_frame_num = dictionary.get(lowest_topic_num)
    except:
        return dictionary
    # convert dictionary to list of tuples
    topic_frame_list = list(dictionary.items()) #[ (topic_num, frame_num)] -> [(1,300),(2,450)]
    topic_frame_list = sorted(topic_frame_list, key=lambda tup: tup[0]) # tup 0 because we are sorting by topic num

    valid_dictionary = {lowest_topic_num : lowest_frame_num}
    previous_topic_num = lowest_topic_num
    previous_frame_num = lowest_frame_num
    
    logger.debug("Lowest Topic Entry: ({}:{})".format(lowest_topic_num,lowest_frame_num))
    
    # append to new dictionary
    for topic_frame in topic_frame_list:
        topic_num = topic_frame[0]
        frame_num = topic_frame[1]
        logger.debug("Current topic Entry: ({}:{})".format(topic_num, frame_num))
        logger.debug("Previous topic Entry: ({}:{})".format(previous_topic_num, previous_frame_num))
        if (topic_num <= previous_topic_num):
            # dont add to dictionary
            logger.debug("Topic number ({}) was <= previous topic number ({}), not adding to valid dictionary!".format(topic_num, previous_topic_num))
            pass
        else:
            # check if the frame number associated with this topic number is bigger than previous topic number
            if (frame_num > previous_frame_num):
                logger.debug("Current Topic Entry is valid, adding ({}:{}) to valid dictinary".format(topic_num,frame_num))
                valid_dictionary[topic_num] = frame_num
                # update previous values
                previous_frame_num = frame_num
                previous_topic_num = topic_num
            else:
                logger.debug("previous frame number ({}) was higher than the current one ({}), not adding to valid dictionary!".format(previous_frame_num, frame_num))
                
    logger.info("Valid Dictionary: {}".format(valid_dictionary))
    return valid_dictionary


# most updated!!
def frame_number_to_time(dictionary, frame_number, frame_rate):
    logger.debug("Getting frame number to time...")
    times_array = list()
    # try needed, for empty dictionary then min will fail
    try: 
        topic_frame_list = list(dictionary.items()) #[ (topic_num, frame_num)] -> [(1,300),(2,450)]
        topic_frame_list = sorted(topic_frame_list, key=lambda tup: tup[0])

        # generate times and add them to the array
        for topic_frame in topic_frame_list:
            topic_num = topic_frame[0]
            frame_num = topic_frame[1]
            time = math.floor(_convert_frame_num_to_time(frame_number=frame_num, frame_rate=frame_rate))
            times_array.append(time)
            logger.debug("Topic Entry: ({}:{}) -> ({})s".format(topic_num, frame_num, time))
    except:
        pass

    # check if the last fraame is in times array, if not then add it
    last_frame_time = math.floor(_convert_frame_num_to_time( frame_number=frame_number, frame_rate=frame_rate))

    if not(last_frame_time in times_array):
        logger.info("Last frame Time ({}) not in times array, adding now".format(last_frame_time))
        times_array.append(last_frame_time)

    logger.info("Times Array: {}".format(times_array))
    return times_array      

# convert a frame number to second
def _convert_frame_num_to_time(frame_number, frame_rate):
    logger.debug("Converting frame number ({}) to time...".format(frame_number))
    return (frame_number/frame_rate)
