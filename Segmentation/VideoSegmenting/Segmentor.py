'''
Script gets all necessary frames and puts them in a list
List of frames can then be used to extract the text
'''
from FileVideoReadFrame import FileVideoReadFrame
from FileVideoReadData import FileVideoReadData
from moviepy.editor import VideoFileClip
from imutils.video import FPS
from threading import Lock
import numpy as np
import argparse
import Sub_Clip
# import myLogger
# import logging
import imutils
import random
import time
import math
import cv2
import os
import re

from PIL import Image, ImageFont, ImageDraw
# from pytesseract import image_to_string
from ExtractIDData import ExtractIDDataQR
from Verifier import CourseCodeVerifier, TopicVerifier
import datetime
import logging
# import MasterEnvironemnt.Logger 


class Segmentor(object):

    Nr_Threads = 1
    logger = logging.getLogger("Logger")


    def __init__(self, video, threshold_frame, threshold_frame_timeout):
        # self.logger.setLevel(logging.DEBUG)                  # change level depending on what you want to see
        self.logger.info("starting video file thread...")

        # replace with something else, like reading a csv file
        self.COURSE_ID_LIST = ['Signals and Communications 2','Signals and Communications 3','Digital Signal Analysis 4','Software Design and Modelling']

        self._initialise_variables(video, threshold_frame, threshold_frame_timeout)
        # start reading frames
        #self.initialise_reading_frames(self.video_dir, self.id_extractor)
        # start extracting data from frames
        #self.initialise_extracting_data(self.fvrf, self.id_extractor)


    def _initialise_variables(self, video, frame_threshold, threshold_frame_timeout):
        self.logger.debug("Initialising Variables...")
        self.dictionary_frame_data = {}
        # used to store the start frame of a QR code
        self.dictionary_start_frame_data = {}   
        self.current_topic_seen = [-1,-1,-1,-1, "" ] # [<topic number>, <first frame seen>, <last frame seen>, <amount seen coninous>]
        self.video_dir = video.get_video_path() 
        self.sub_clip_dir = video.get_destination_directory()
        # We are using the QR decoding procedure
        self.id_extractor = ExtractIDDataQR()
        # save the video of the video we are segmenting
        self.video = video
        # we are encoding the data via its course_code index, thus use CourseCodeVerifier
        self.verifier = CourseCodeVerifier(video)
        # self.verifier = TopicVerifier(video)
        # start the FPS timer
        self.fps = video.get_frame_rate()
        # self.THRESHOLD_FRAME = frame_threshold  # ~4s
        self.THRESHOLD_FRAME_CONTINUOUS = frame_threshold
        self.THRESHOLD_FRAME_TIMEOUT = threshold_frame_timeout #30
        self.logger.debug("Initialise Variables Successfully")


    def _initialise_reading_frames(self):
        self.logger.info("Reading Frames")
        # start grabbing frames
        self.fvrf = FileVideoReadFrame(self.video_dir, self.id_extractor).start()
        # wait until the frames start getting proccessed
        while self.fvrf.Q.qsize()!=self.fvrf.q_size:
            pass
        self.logger.debug("Reading Frames Successful")


    # start all the threads to extract the data
    def _start_extracting_data(self):
        fvrf = self.fvrf
        id_extractor = self.id_extractor
        self.logger.info("Initialising Extracting Data")
        self.lock = Lock()
        self.fvrd = []
        # save the fvr into a list
        for i in range(self.Nr_Threads):
            self.fvrd.append(FileVideoReadData(fvrf, i, self, id_extractor).start())

        self.logger.info("Initialised Extractors Successfully")

    # def update_text_dictionary(self, data, frame_number, frame):
    #     self.logger.debug("Checking data: ({}), frame_number: {}".format(data,frame_number))
    #     # use lock so only one FVR thread can update dictionary at a time
    #     # need to change how we check if data is valid
    #     self.lock.acquire()
    #     try:
    #         # we are checking that the data we have is what we expect
    #         if (not (self.verifier.verify(data))):
    #             # self.logger.debug("Data not verified")
    #             return
    #         key_data = self.verifier.get_data_index(data)
    #         #check if topic number already in dictionary, if not then add it
    #         if (key_data in self.dictionary_frame_data):
    #             self.logger.debug("Key data ({}) already in frame data dictionary".format(key_data))
    #             saved_frame_number = self.dictionary_frame_data[key_data]
    #             #if (saved_frame_number < frame_number):
    #                 # need to add conditional so that it if we see QR code 10 mins after previously seen, we ignore it
    #             if ( (saved_frame_number < frame_number) and (frame_number - saved_frame_number < self.THRESHOLD_FRAME_TIMEOUT) ):
    #                 self.dictionary_frame_data[key_data] = frame_number
    #                 # check if any topics we have saved in this dict that are bigger than the current topic number. if so then delete them
    #                 self._remove_higher_topics(self.dictionary_frame_data, key_data)
                    
    #                 self.logger.debug("Updated frame data ({}) dictionary with new index {} vs old index {}".format(key_data, frame_number, saved_frame_number))
    #         else:
    #             self.logger.info("Key data ({}:{}) not in frame data dictionary, adding entry now...".format(key_data,frame_number))
    #             self.dictionary_frame_data[key_data] = frame_number
    #             # enter 
    #             self.dictionary_start_frame_data[key_data] = frame_number

    #     # only one thread can execute code there
    #     finally:
    #         self.lock.release() 

    #     self.logger.debug("Dictionary:\n{}\n".format(self.dictionary_frame_data))
    
    def update_text_dictionary(self, data, frame_number, frame):
        self.logger.debug("Checking data: ({}), frame_number: {}".format(data,frame_number))
        # use lock so only one FVR thread can update dictionary at a time
        # need to change how we check if data is valid
        self.lock.acquire()
        # -------------------------------------------------------------
        last_topic_seen = self.current_topic_seen[0]
        frame_number_topic_started_at = self.current_topic_seen[1]
        frame_number_topic_current_at = self.current_topic_seen[2]
        frame_number_continous_topic_seen = self.current_topic_seen[3]
        last_frame_data = self.current_topic_seen[4]
        # -------------------------------------------------------------
        try:    
            key_data = self.verifier.get_data_index(data)    
            # if current key data = last topic seen then update topic_current and continous
            if (key_data == last_topic_seen):
                self.logger.debug("Key data ({}) is same as key data from last entry, updating topic seen array".format(key_data))
                self.current_topic_seen[2] = frame_number
                self.current_topic_seen[3] = self.current_topic_seen[3] + 1
                return
            else:
                self.logger.info("Key data ({}) has changed from {} -> {}".format(key_data, last_topic_seen, key_data))
                # we only care about adding valid data to the dictionary
                if (self.verifier.verify(last_frame_data)):
                    self.logger.info("Data ({}) is valid, going to check the topic seen array to see if valid QR code seen".format(last_frame_data))
                    self.dictionary_frame_data = _add_topic_frame_values(self.dictionary_frame_data,  last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen,self.THRESHOLD_FRAME_CONTINUOUS, self.THRESHOLD_FRAME_TIMEOUT)
                self.logger.info("Data ({}) is invalid not updating frame data dictionary".format(data))
                # update the new values for self.current_topic_seen
                self.current_topic_seen[0] = key_data
                self.current_topic_seen[1] = frame_number
                self.current_topic_seen[2] = frame_number
                self.current_topic_seen[3] = 0
                self.current_topic_seen[4] = data
                return 

        # only one thread can execute code there
        finally:
            self.lock.release()    

    def start(self):
    # loop over frames from the video file stream
        self.logger.debug("Starting Segmention")
        # start reading frames
        self._initialise_reading_frames()
        # start extracting data from frames
        self._start_extracting_data()
        
        # wait until all the frames have been proccessed
        while self.fvrf.more():
            pass

        self.logger.debug('Shutting Down... ')
        # self.time_finish = time.time()
        frame_stamp = self.stop()
        return frame_stamp

    # shut down all the reading data threads
    def _stop_fvrd(self):
        self.logger.debug("Stopping the File Video Read Data threads...")
        for reader in (self.fvrd):
            reader.stop()
            # reader.stopped = True
        # wait until all threads have stopped!
        while True:
            threads_alive = False
            for reader in (self.fvrd): 
                threads_alive = threads_alive & reader.stopped
                self.logger.debug("Thread Frame Reader ({}), Alive = ({})".format(reader.thread_number, reader.stopped))
            if (threads_alive == False):
                break

        self.logger.info("All reader threads stopped, final thread read {}".format(self.fvrf.counter))
        
    # returns the dictionary for topic numbers which appear for longer than THRESHOLD_FRAME (4s)
    # def _get_valid_threshold_frame_dictionary(self, dictionary_frame_start, dictionary_frame_end):
    #     self.logger.info("Creating valid threshold dictionary")
    #     for topic_number, frame_start in dictionary_frame_start.items():
    #         # should exist but maybe error during debugging since frame_end_dict not properly updated
    #         frame_end = dictionary_frame_end[topic_number]
    #         if (frame_end < frame_start + self.THRESHOLD_FRAME):
    #             # remove topic number from dictionary
    #             self.logger.info("Topic {} seen first at frame {} and last seen at frame {}, the difference is below threshold {}. Removing!".format(topic_number, frame_start, frame_end, self.THRESHOLD_FRAME))
    #             del dictionary_frame_end[topic_number]
    #     return dictionary_frame_end


    # ends the Segmentation
    def stop(self):
        # stop the timer and display FPS information
        # self.fpsself.fps.stop()
        self.logger.info("[BEFORE] Videos Number of Frames: {}, Number of Read Frames; {}".format(self.video.get_number_of_frames(),self.fvrf.frame_number ))
        self.video.set_number_of_frames(self.fvrf.frame_number) #cv2 get frames seems to be a bit iffy and we choose either our 
                                           #calculated or cv2, choosing our calculated
        self.logger.info("[AFTER] Videos Number of Frames: {}, Number of Read Frames; {}".format(self.video.get_number_of_frames(),self.fvrf.frame_number ))
        self._stop_fvrd()

        # remove topic numbers which have only appeared for less than THRESHOLD_FRAME
        #self.dictionary_frame_data = self._get_valid_threshold_frame_dictionary(self.dictionary_start_frame_data, self.dictionary_frame_data)
        if (-1 in self.dictionary_frame_data):
            del self.dictionary_frame_data[-1]

        self.video.frame_stamp = self.dictionary_frame_data
        return (self.dictionary_frame_data)

logger_test = logging.getLogger("Logger")

def _add_topic_frame_values(dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT):
    frame_data_dictionary = dictionary.copy()
    # check if meets continous requirements
    if (frame_number_continous_topic_seen >= THRESHOLD_FRAME_CONTINUOUS):
        logger_test.debug("Topic is SUCCESSFULLY continuous")
        # check if meets requirements for being within 10s of same topic number
        if (last_topic_seen in frame_data_dictionary):
            logger_test.debug("Topic seen in frame dictionary")
            # it has been seen, has it been less than 10s since then?
            dictionary_topic_stored_frame = frame_data_dictionary[last_topic_seen]
            # check if first time we started seeing this data is within 10s of last seen it before
            if (frame_number_topic_started_at - dictionary_topic_stored_frame < THRESHOLD_FRAME_TIMEOUT):
                logger_test.info("Topic ({}) is within time out, adding!".format(last_topic_seen))
                # YES it is within 10s therefore add it to the dictionary
                frame_data_dictionary[last_topic_seen] = frame_number_topic_current_at
                logger_test.debug("Frame Dictionary before removing higher topics: {}".format(frame_data_dictionary))
                # not remove any topics seen after this
                frame_data_dictionary = _remove_higher_topics(frame_data_dictionary,last_topic_seen)
                logger_test.debug("Frame Dictionary after removing higher topics: {}".format(frame_data_dictionary))
            else:
                logger_test.debug("Topic is not within timeout, not adding")
                # no it is not within 10s therefor do not add it
                pass
        # it has not been seen in dictionary,
        else:
            # pretty sure i can just add it to dictionary without needing to check it
            logger_test.debug("Topic has not been seen in dictionary")
            # check if the first time we seen this and last time is greater than continuous threshold
            if (frame_number_topic_current_at - frame_number_topic_started_at > THRESHOLD_FRAME_CONTINUOUS):
                logger_test.debug("Topic is successfully continuous, adding it")
                # add it to the dictionary
                frame_data_dictionary[last_topic_seen] = frame_number_topic_current_at
            else:
                # since it is not more than the continous threshold ignore it
                logger_test.debug("Topic is unsuccessfully continuous, not adding it")
                pass
    #logger_test.debug("Topic is unsuccessfully continuous, not adding it")
    return frame_data_dictionary


# removes any entries whose topic number is bigger than the given one
def _remove_higher_topics(dictionary, topic_number):
    new_dictionary = dictionary.copy()
    for key,value in dictionary.items():
        # check if the key is bigger than current topic number,
        # if so then delete it
        if (key > topic_number):
            del new_dictionary[key]
            logger_test.debug("Removing Key: {} from dictionary".format(key))
    logger_test.debug("Dictionary being returned: {}".format(new_dictionary))
    return new_dictionary

if __name__ == "__main__":
    cwd = os.getcwd()
    video_dir_SDM_13 = 'SDM_13.5min_Trim.mp4'
