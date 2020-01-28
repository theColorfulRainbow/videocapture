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


    def __init__(self, video, threshold_frame):
        # self.logger.setLevel(logging.DEBUG)                  # change level depending on what you want to see
        self.logger.info("starting video file thread...")

        # replace with something else, like reading a csv file
        self.COURSE_ID_LIST = ['Signals and Communications 2','Signals and Communications 3','Digital Signal Analysis 4','Software Design and Modelling']

        self.initialise_variables(video, threshold_frame)
        # start reading frames
        self.initialise_reading_frames(self.video_dir, self.id_extractor)
        # start extracting data from frames
        #self.initialise_extracting_data(self.fvrf, self.id_extractor)


    def initialise_variables(self, video, frame_threshold):
        self.logger.debug("Initialising Variables...")
        self.dictionary_frame_data = {}
        # used to store the start frame of a QR code
        self.dictionary_start_frame_data = {}   
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
        self.THRESHOLD_FRAME = frame_threshold  # ~4s
        self.logger.debug("Initialise Variables Successfully")


    def initialise_reading_frames(self, video_dir, id_extractor):
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

        self.logger.debug("Initialised Extractors Successfully")

    def update_text_dictionary(self, data, frame_number, frame):
        self.logger.debug("Checking data: ({}), frame_number: {}".format(data,frame_number))
        # use lock so only one FVR thread can update dictionary at a time
        # need to change how we check if data is valid
        self.lock.acquire()
        # print("In Update dictionary")
        try:
            # check we are only adding topic.nr to our dictionary and not every slides text
            # if (not ('Topic nr.' in data)):
            #         return
            # we are checking that the data we have is what we expect
            if (not (self.verifier.verify(data))):
                # self.logger.debug("Data not verified")
                return
            key_data = self.verifier.get_data_index(data)
            #check if topic number already in dictionary, if not then add it
            if (key_data in self.dictionary_frame_data):
                self.logger.debug("Key data ({}) already in frame data dictionary".format(key_data))
                saved_frame_number = self.dictionary_frame_data[key_data]
                if (saved_frame_number < frame_number):
                    # need to add conditional so that it if we see QR code 10 mins after previously seen, we ignore it
                    # if ( (saved_frame_number < frame_number) and (frame_number - saved_frame_number < 30000) ):
                    self.dictionary_frame_data[key_data] = frame_number
                    self.logger.debug("Updated frame data ({}) dictionary with new index {} vs old index {}".format(key_data, frame_number, saved_frame_number))
            else:
                self.logger.info("Key data ({}:{}) not in frame data dictionary, adding entry now...".format(key_data,frame_number))
                self.dictionary_frame_data[key_data] = frame_number
                # enter 
                self.dictionary_start_frame_data[key_data] = frame_number
        # only one thread can execute code there
        finally:
            self.lock.release() #release lock
        # replace with logger
        self.logger.debug("Dictionary:\n{}\n".format(self.dictionary_frame_data))


    def start(self):
    # loop over frames from the video file stream
        self.logger.debug("Starting Segmention")
        self._start_extracting_data()
        # self.fps.update()
        # self.time_start = time.time()
        # wait until all the frames have been proccessed
        while self.fvrf.more():
            pass

        self.logger.debug('Shutting Down... ')
        # self.time_finish = time.time()
        frame_stamp = self.stop()
        return frame_stamp

    # shut down all the threads
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


    # creates the sub clips
    def _create_sub_clips(self,video_dir, sub_clip_dir, times_array, course_name):
        self.logger.debug("Creating sub clips...")
        Sub_Clip.create_subClips(self.video_dir, self.sub_clip_dir, times_array, course_name)


    # returns the dictionary for topic numbers which appear for longer than THRESHOLD_FRAME (4s)
    def _get_valid_threshold_frame_dictionary(self, dictionary_frame_start, dictionary_frame_end):
        self.logger.info("Cretaing valid threshold dictionary")
        for topic_number, frame_start in dictionary_frame_start.items():
            # should exist but maybe error during debugging since frame_end_dict not properly updated
            frame_end = dictionary_frame_end[topic_number]
            if (frame_end < frame_start + self.THRESHOLD_FRAME):
                # remove topic number from dictionary
                self.logger.info("Topic {} seen first at frame {} and last seen at frame {}, the difference is below threshold {}. Removing!".format(topic_number, frame_start, frame_end, self.THRESHOLD_FRAME))
                del dictionary_frame_end[topic_number]
        return dictionary_frame_end


    # ends the Segmentation
    def stop(self):
        # stop the timer and display FPS information
        # self.fpsself.fps.stop()
        self.logger.info("[BEFORE] Videos Number of Frames: {}, Number of Read Frames; {}".format(self.video.get_number_of_frames(),self.fvrf.frame_number ))
        self.video.set_number_of_frames(self.fvrf.frame_number) #cv2 get frames seems to be a bit iffy and we choose either our 
                                           #calculated or cv2, choosing our calculated
        self.logger.info("[AFTER] Videos Number of Frames: {}, Number of Read Frames; {}".format(self.video.get_number_of_frames(),self.fvrf.frame_number ))
        self._stop_fvrd()

        # self.logger.info("elasped time: {:.2f}".format(self.fps.elapsed()))
        # self.logger.info("time taken: {}".format(self.time_finish-self.time_start))
        # self.logger.info("approx. FPS: {:.2f}".format(self.fps.fps()))
        # convert frame_numbers in dictionary to time in video
        # times_array = self._frame_number_to_time(self.dictionary_frame_data)

        # # pass times as list to sub_clips.py
        # self.video.set_time_array(times_array)
        # self.video.set_topic_frame_dict(self.dictionary_frame_data)
        # self.video.set_number_of_frames(self.fvrf.frame_number)
        # remove topic numbers which have only appeared for less than THRESHOLD_FRAME
        self.dictionary_frame_data = self._get_valid_threshold_frame_dictionary(self.dictionary_start_frame_data, self.dictionary_frame_data)
        self.video.frame_stamp = self.dictionary_frame_data
        
        # self.logger.debug("Frame Stamp Ordered Dictionary: {}".format(ordered_dictionary))
        return (self.dictionary_frame_data)


if __name__ == "__main__":
    cwd = os.getcwd()
    video_dir_SDM_13 = 'SDM_13.5min_Trim.mp4'
