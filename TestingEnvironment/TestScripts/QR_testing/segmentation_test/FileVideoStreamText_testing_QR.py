'''
Script/Class that creates threads and returns the frame (class) of video sequence
'''
# import the necessary packages
from threading import Thread
import sys
import cv2
import numpy as np

from PIL import Image, ImageFont, ImageDraw
from pytesseract import image_to_string

import pyzbar.pyzbar as pyzbar

class FileVideoRead:
    def __init__(self, fvs, thread_number, main_thread):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stopped = False
        # the video file
        self.fvs = fvs
        self.thread_number = thread_number
        self.main_thread = main_thread

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.readFrame, args=())
        t.daemon = True
        t.start()
        return self

    def get_frame_txt(self, frame):
        img_arr = Image.fromarray(frame)        # convert from array to image
        img_arr_grey = img_arr.convert('L')     # use grey converter (greyscale)
        img_arr_thresh = img_arr_grey.point(lambda x: 0 if 0<=x<=150 else 256) # set threshold for black and white 
        frame_txt = image_to_string(img_arr_thresh)                            # get text from black and white image
        return frame_txt

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
            

            # cur_frame_txt = self.get_frame_txt(frame) # Getting text using tesseract-ocr

            # ----------------------- TESTING QR  --------------------------------
            cur_frame_txt = 'NO QR DETECTED'
            decodedFrame = pyzbar.decode(image)
            for obj in decodedFrame:
                cur_frame_txt = obj.data.decode('utf-8')
                print(cur_frame_txt)  
            #---------------------------------------------------------------------


            self.main_thread.update_text_dictionary(cur_frame_txt,frame_number)
            #print('In While loop and current frame number = ' + str(frame_number)) 
        

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True