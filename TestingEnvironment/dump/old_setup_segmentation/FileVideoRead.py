'''
Script/Class that creates threads and returns the frame (class) of video sequence
'''
# import the necessary packages
from threading import Thread
import cv2
import numpy as np

from PIL import Image, ImageFont, ImageDraw

class FileVideoReadData:
    def __init__(self, fvs, thread_number, main_thread,id_extractor):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stopped = False
        # the video file
        self.fvs = fvs
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
        while self.fvs.more():
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            frame, frame_number = self.fvs.read() #get frame
            # convert frame to text
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])
            frame_data = self.id_extractor.get_data(frame)
            # send text from tesseract to update text dict
            self.main_thread.update_text_dictionary(cur_frame_txt,frame_number,frame)


    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
