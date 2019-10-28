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
import datetime

class Segmentor(object):

    Nr_Threads = 1

    def __init__(self, video_dir, sub_clip_dir):
        print("[INFO] starting video file thread...")

        # replace with something else, like reading a csv file
        self.COURSE_ID_LIST = ['Signals and Communications 2','Signals and Communications 3','Digital Signal Analysis 4','Software Design and Modelling']

        self.initialise_variables(video_dir, sub_clip_dir)
        # start reading frames
        self.initialise_reading_frames(self.video_dir, self.id_extractor)
        # start extracting data from frames
        self.initialise_extracting_data(self.fvrf, self.id_extractor)


    def initialise_variables(self, video_dir, sub_clip_dir):
        self.dictionary_frame_text = {}
        self.video_dir = video_dir
        # We are using the QR decoding procedure
        self.id_extractor = ExtractIDDataQR()
        # start the FPS timer
        self.fps = FPS().start()
        # better to get exact frame rate from cv2 but seems to break this code/tesseract
        self.frame_rate = 29.975#self.get_frame_rate(video_dir)
        self.sub_clip_dir = sub_clip_dir

    def initialise_reading_frames(self, video_dir, id_extractor):
        print('STARTING READING FRAMES')
        # start grabbing frames
        self.fvrf = FileVideoReadFrame(self.video_dir, self.id_extractor).start()
        # wait until the frames start getting proccessed
        while self.fvrf.Q.qsize()!=self.fvrf.q_size:
            pass


    # initialise all the threads to extract the data
    def initialise_extracting_data(self, fvrf, id_extractor):
        print('STARTING READING DATA')
        self.lock = Lock()
        self.fvrd = []
        # save the fvr into a list
        for i in range(self.Nr_Threads):
            self.fvrd.append(FileVideoReadData(fvrf, i, self, id_extractor).start())

        # start the fvr(s)
        # for reader in (self.fvrd):
        #     reader.start()

    def update_text_dictionary(self, data, frame_number, frame):
        # use lock so only one FVR thread can update dictionary at a time
        # need to change how we check if data is valid
        self.lock.acquire()
        # print("In Update dictionary")
        try:
            # check we are only adding topic.nr to our dictionary and not every slides text
            if (not ('Topic nr.' in data)):
                    return
            # update the dictionary
            if data in self.dictionary_frame_text:
                saved_frame_number = self.dictionary_frame_text[data]
                if saved_frame_number < frame_number:
                    self.dictionary_frame_text[data] = frame_number
            else:
                self.dictionary_frame_text[data] = frame_number
        # only one thread can execute code there
        finally:
            self.lock.release() #release lock
        # replace with logger
        print('DICTIONARY:\n{}\n'.format(self.dictionary_frame_text))


    def start(self):
    # loop over frames from the video file stream
        converter_del = 0
        self.fps.update()
        self.time_start = time.time()

        # wait until all the frames have been proccessed
        while self.fvrf.more():
            pass

        print('Shutting Down... ')
        self.time_finish = time.time()
        self.stop()


    def _get_frame_rate(self,clip):
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
        times_array = list()
        for topic in dictionary:
            time = math.floor(self._convert_frame_num_to_time( frame_number=dictionary[topic], frame_rate=self.frame_rate))
            times_array.append(time)

        # check if the last fraame is in times array, if not then add it
        last_frame_time = math.floor(self._convert_frame_num_to_time( frame_number=self.fvrf.frame_number, frame_rate=self.frame_rate))
        print('dictionary = {}\ntimes_array = {}\nlast frame number = {} last_frame_time={}'.format(dictionary,times_array,self.fvrf.frame_number,last_frame_time))

        if not(last_frame_time in times_array):
            times_array.append(last_frame_time)

        print('FINAL: times_array = {}\nlast_frame_time={}'.format(times_array,last_frame_time))
        return times_array

    # convert a frame number to second
    def _convert_frame_num_to_time(self, frame_number, frame_rate):
        return (frame_number/frame_rate)


    # orders the dictionary with regartds to the frame number
    def _orderDictionary(self, dictionary):
        ordered_dictionary = sorted(dictionary, key=dictionary.get, reverse=False)
        return ordered_dictionary

    # returns the course name found in the dictionary keys, should do this in another class
    def _get_course_name(self,dictionary):
        text, frame = random.choice(list(dictionary.items()))
        course_name = ''
        for course_id in self.COURSE_ID_LIST:
            if (course_id in text):
                course_name = course_id
            else:
                print('{} not in {}'.format(course_id,text))
        print('course_name = {}'.format(course_name))
        return course_name

    # returns the dictionary of text to frame
    def getDictionary(self):
        return self.dictionary_frame_text

    # shut down all the threads
    def _stop_fvrd(self):
        for reader in (self.fvrd):
            reader.stop()
            reader.stopped = True

    # creates the sub clips
    def _create_sub_clips(self,video_dir, sub_clip_dir, times_array, course_name):
        Sub_Clip.create_subClips(self.video_dir, self.sub_clip_dir, times_array, course_name)

    def stop(self):
        # stop the timer and display FPS information
        self.fps.stop()
        self._stop_fvrd()

        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print('[INFO] self.time_finish-self.time_start: {}'.format(self.time_finish-self.time_start))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()

        print ('-' * 60)
        print (self.dictionary_frame_text)
        print ('-' * 60)

        # make sure the dictionary is in ascending order, with no skips else raise exception
        ordered_dictionary = self._orderDictionary(self.dictionary_frame_text)
        print ('-' * 60)
        print (ordered_dictionary)
        print(self.dictionary_frame_text)
        print ('-' * 60)

        # make sure there are no skips in the topic numbers

        # convert frame_numbers in dictionary to time in video
        times_array = self._frame_number_to_time(self.dictionary_frame_text)

        print ('-' * 60)
        print (times_array)
        print ('-' * 60)
        course_name = self._get_course_name(self.dictionary_frame_text)
        # pass times as list to sub_clips.py
        self._create_sub_clips(self.video_dir, self.sub_clip_dir, times_array, course_name)

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
