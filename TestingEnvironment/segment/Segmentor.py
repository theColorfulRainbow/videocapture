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
from Verifier import CourseCodeVerifier
import datetime
import logging
import Logger

class Segmentor(object):

    Nr_Threads = 1
    logger = logging.getLogger("Logger")


    def __init__(self, video_dir, sub_clip_dir, video):
        # self.logger.setLevel(logging.DEBUG)                  # change level depending on what you want to see
        self.logger.info("starting video file thread...")

        # replace with something else, like reading a csv file
        self.COURSE_ID_LIST = ['Signals and Communications 2','Signals and Communications 3','Digital Signal Analysis 4','Software Design and Modelling']

        self.initialise_variables(video_dir, sub_clip_dir, video)
        # start reading frames
        self.initialise_reading_frames(self.video_dir, self.id_extractor)
        # start extracting data from frames
        self.initialise_extracting_data(self.fvrf, self.id_extractor)


    def initialise_variables(self, video_dir, sub_clip_dir, video):
        self.logger.debug("Initialising Variables...")
        self.dictionary_frame_data = {}
        self.video_dir = video_dir
        # We are using the QR decoding procedure
        self.id_extractor = ExtractIDDataQR()
        # save the video of the video we are segmenting
        self.video = video
        # we are encoding the data via its course_code index, thus use CourseCodeVerifier
        self.verifier = CourseCodeVerifier(video)
        # start the FPS timer
        self.fps = FPS().start()
        # better to get exact frame rate from cv2 but seems to break this code/tesseract
        self.frame_rate = 29.975#self.get_frame_rate(video_dir)
        self.sub_clip_dir = sub_clip_dir
        self.logger.debug("Initialise Variables Successfully")

    def initialise_reading_frames(self, video_dir, id_extractor):
        self.logger.info("Reading Frames")
        # start grabbing frames
        self.fvrf = FileVideoReadFrame(self.video_dir, self.id_extractor).start()
        # wait until the frames start getting proccessed
        while self.fvrf.Q.qsize()!=self.fvrf.q_size:
            pass
        self.logger.debug("Reading Frames Successful")

    # initialise all the threads to extract the data
    def initialise_extracting_data(self, fvrf, id_extractor):
        self.logger.info("Initialising Extracting Data")
        self.lock = Lock()
        self.fvrd = []
        # save the fvr into a list
        for i in range(self.Nr_Threads):
            self.fvrd.append(FileVideoReadData(fvrf, i, self, id_extractor).start())

        self.logger.debug("Initialised Extractors Successfully")

    def update_text_dictionary(self, data, frame_number, frame):
        self.logger.debug("Updating text Dictionary with data: {}, frame_number: {}".format(data,frame_number))
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

            key_data = data
            if (key_data in self.dictionary_frame_data):
                self.logger.debug("Key data already in frame data dictionary")
                saved_frame_number = self.dictionary_frame_data[key_data]
                if (saved_frame_number < frame_number):
                    self.dictionary_frame_data[key_data] = frame_number
                    self.logger.debug("Updated frame data dictionary with new index {} vs old index {}",format(fame_number, saved_frame_number))
            else:
                self.logger.debug("Key data not in frame data dictionary, adding entry now...")
                self.dictionary_frame_data[key_data] = frame_number
            # update the dictionary
            # if data in self.dictionary_frame_data:
            #     saved_frame_number = self.dictionary_frame_data[data]
            #     if saved_frame_number < frame_number:
            #         self.dictionary_frame_data[data] = frame_number
            # else:
            #     self.dictionary_frame_data[data] = frame_number
        # only one thread can execute code there
        finally:
            self.lock.release() #release lock
        # replace with logger
        self.logger.debug("DICTIONARY:\n{}\n".format(self.dictionary_frame_data))


    def start(self):
    # loop over frames from the video file stream
        self.logger.debug("Starting Segmention")
        converter_del = 0
        self.fps.update()
        self.time_start = time.time()

        # wait until all the frames have been proccessed
        while self.fvrf.more():
            pass

        self.logger.debug('Shutting Down... ')
        self.time_finish = time.time()
        self.stop()


    def _get_frame_rate(self,clip):
        self.logger.debug("Getting frame rate...")
        moviepy_clip = VideoFileClip(clip)
        cap = cv2.VideoCapture(clip)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        clip_fps = length/moviepy_clip.duration
        cap.release()
        del moviepy_clip
        del cap
        return clip_fps

    # most updated!!
    def _frame_number_to_time(self, dictionary):
        self.logger.debug("Getting frame number to time...")
        times_array = list()
        for topic in dictionary:
            time = math.floor(self._convert_frame_num_to_time( frame_number=dictionary[topic], frame_rate=self.frame_rate))
            times_array.append(time)

        # check if the last fraame is in times array, if not then add it
        last_frame_time = math.floor(self._convert_frame_num_to_time( frame_number=self.fvrf.frame_number, frame_rate=self.frame_rate))
        self.logger.debug('dictionary = {}\ntimes_array = {}\nlast frame number = {} last_frame_time={}'.format(dictionary,times_array,self.fvrf.frame_number,last_frame_time))

        if not(last_frame_time in times_array):
            times_array.append(last_frame_time)

        self.logger.debug('times_array = {}\nlast_frame_time={}'.format(times_array,last_frame_time))
        return times_array

    # convert a frame number to second
    def _convert_frame_num_to_time(self, frame_number, frame_rate):
        self.logger.debug("Converting frame number to time...")
        return (frame_number/frame_rate)


    # orders the dictionary with regartds to the frame number
    def _orderDictionary(self, dictionary):
        self.logger.debug("Ordering the Dictionary")
        ordered_dictionary = sorted(dictionary, key=dictionary.get, reverse=False)
        return ordered_dictionary

    # returns the course name found in the dictionary keys, should do this in another class
    def _get_course_name(self,dictionary):
        self.logger.debug("Getting course name...")
        text, frame = random.choice(list(dictionary.items()))
        course_name = ''
        for course_id in self.COURSE_ID_LIST:
            if (course_id in text):
                course_name = course_id
            else:
                self.logger.debug('{} not in {}'.format(course_id,text))
        self.logger.debug('course_name: {}'.format(course_name))
        return course_name

    # returns the dictionary of text to frame
    def getDictionary(self):
        return self.dictionary_frame_data

    # shut down all the threads
    def _stop_fvrd(self):
        self.logger.debug("Stopping the File Video Read Data threads...")
        for reader in (self.fvrd):
            reader.stop()
            reader.stopped = True

    # creates the sub clips
    def _create_sub_clips(self,video_dir, sub_clip_dir, times_array, course_name):
        self.logger.debug("Creating sub clips...")
        Sub_Clip.create_subClips(self.video_dir, self.sub_clip_dir, times_array, course_name)

    def stop(self):
        # stop the timer and display FPS information
        self.fps.stop()
        self._stop_fvrd()

        self.logger.info("elasped time: {:.2f}".format(self.fps.elapsed()))
        self.logger.info("time taken: {}".format(self.time_finish-self.time_start))
        self.logger.info("approx. FPS: {:.2f}".format(self.fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()

        # print ('-' * 60)
        self.logger.info(self.dictionary_frame_data)
        # print ('-' * 60)

        # make sure the dictionary is in ascending order, with no skips else raise exception
        ordered_dictionary = self._orderDictionary(self.dictionary_frame_data)
        # print ('-' * 60)
        self.logger.info("Ordered Dictionary: {}".format(ordered_dictionary))
        self.logger.info("Key Data -> frame number dictionary: {}".format(self.dictionary_frame_data))
        # print ('-' * 60)

        # make sure there are no skips in the topic numbers

        # convert frame_numbers in dictionary to time in video
        times_array = self._frame_number_to_time(self.dictionary_frame_data)

        # print ('-' * 60)
        self.logger.info("Times Array: {}".format(times_array))
        # print ('-' * 60)
        video_name = self.video.get_video_name()
        # pass times as list to sub_clips.py
        self._create_sub_clips(self.video_dir, self.sub_clip_dir, times_array, video_name)

if __name__ == "__main__":
    cwd = os.getcwd()
    video_dir_SDM_13 = 'SDM_13.5min_Trim.mp4'
    # trimed Video
    # timings_class = GetTimings('C:\\Users\\ilieg\\Desktop\\Scripts\\videcapture-master_summer\\Lecture Downloading\\2017-2018\\SCEE08007\\2019-08-02T14.09.00.000Z\\primary.mp4',cwd)
    timings_class = GetTimings(video_dir_SDM_13,cwd)
    # full video
    # timings_class = GetTimings('C:\\Users\\Gabi\\Desktop\\Ilie\\videcapture-master\\Testing\\small_video_tst_25s.mp4',cwd)
    # Visualizer video --- can only be detected using SSIM (get_SSIM_topic_number)
    # timings_class = GetTimings('C:\\Users\\Gabi\\Desktop\\Ilie\\videcapture-master\\Lecture Downloading\\2017-2018\\SCEE08007\\2019-08-02T14.09.00.000Z\\Visualizer.mp4',cwd)
    timings_class.start()
