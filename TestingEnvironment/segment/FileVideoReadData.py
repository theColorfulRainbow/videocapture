'''
Script/Class that creates threads and returns the frame (class) of video sequence
'''
# import the necessary packages
from threading import Thread
import cv2
import numpy as np
import Logger
import logging
from PIL import Image, ImageFont, ImageDraw

class FileVideoReadData(object):
    def __init__(self, fvrf, thread_number, main_thread,id_extractor):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.logger = logging.getLogger("Logger")
        self.stopped = False
        # the video file
        self.fvrf = fvrf
        self.thread_number = thread_number
        self.main_thread = main_thread
        self.id_extractor = id_extractor


    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.readFrame, args=())
        t.daemon = True
        t.start()
        return self

    def readFrame(self):
        # keep looping infinitely
        # print("in read frame")
        while self.fvrf.more():
            # print("in while of read frame")
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            frame, frame_number = self.fvrf.read() #get frame
            # convert frame to text
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame = np.dstack([frame, frame, frame])
            frame_data = self.id_extractor.get_data(frame)
            # print("Getting frame")
            # data from id_extractor
            self.main_thread.update_text_dictionary(frame_data,frame_number,frame)


    # stops reading the frames
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
