'''
Script gets all necessary frames and puts them in a list
List of frames can then be used to extract the text 
'''
from FileVideoStream import FileVideoStream
from FileVideoStreamText import FileVideoRead
from moviepy.editor import VideoFileClip
from imutils.video import FPS
from threading import Lock
import numpy as np
import argparse
import Sub_Clip
import imutils
import time
import cv2
import os

from PIL import Image, ImageFont, ImageDraw
from pytesseract import image_to_string
import datetime

class GetTimings(object):
    def __init__(self, video_dir, sub_clip_dir):
        self.dictionary_frame_text = {}
        self.video_dir = video_dir
        print("[INFO] starting video file thread...")
        self.fvs = FileVideoStream(self.video_dir).start()
        time.sleep(1.0)
        # start the FPS timer
        self.fps = FPS().start()
        # initialising the threads for getting the text from frames
        for i in range(10):
            self.fvr = FileVideoRead(self.fvs,i,self).start()
        self.lock = Lock()
        self.frame_rate = 29.975#self.get_frame_rate(video_dir)
        self.sub_clip_dir = sub_clip_dir


    def get_frame_txt(self, frame):
        img_arr = Image.fromarray(frame)        # convert from array to image
        img_arr_grey = img_arr.convert('L')     # use grey converter (greyscale)
        
        img_arr_thresh = img_arr_grey.point(lambda x: 0 if 0<=x<=150 else 256) # set threshold for black and white 
        frame_txt = image_to_string(img_arr_thresh)                            # get text from black and white image
        return frame_txt

    def update_text_dictionary(self, text, frame_number):

        # use lock so only one FVR thread can update dictionary at a time
        self.lock.acquire()
        try:
            # check we are only adding topic.nr to our dictionary and not every slides text
            if (not ('Topic nr.' in text)):
                    return
            # update the dictionary
            if text in self.dictionary_frame_text:
                saved_frame_number = self.dictionary_frame_text[text]
                if saved_frame_number < frame_number: 
                    self.dictionary_frame_text[text] = frame_number
            else:
                self.dictionary_frame_text[text] = frame_number
        
        # only one thread can execute code there
        finally:
            self.lock.release() #release lock


    def start(self):
    # loop over frames from the video file stream
        converter_del = 0
        while self.fvs.more():
            print('counter:',converter_del)
            converter_del += 1
            frame, frame_number = self.fvs.read() #get frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = np.dstack([frame, frame, frame])    
            frame_txt = self.get_frame_txt(frame)   # Frame text using tesseract
            #print('frame_number = {}\ncur_frame_txt:\n{}'.format(frame_number,main_thread_frame_txt))
            self.update_text_dictionary(frame_txt,frame_number)
            #print('In While loop and current frame number = ' + str(frame_number))
            self.fps.update()
            
            
        # stop the timer and display FPS information
        self.fps.stop()
        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps())) 
        # do a bit of cleanup
        cv2.destroyAllWindows()
        self.fvs.stop()
        
        print ('=' * 60)
        print (self.dictionary_frame_text)
        print ('=' * 60)

        # make sure the dictionary is in ascending order, with no skips else raise exception
        ordered_dictionary = self.orderDictionary(self.dictionary_frame_text)
        print ('%' * 60)
        print (ordered_dictionary)
        print(self.dictionary_frame_text)
        print ('%' * 60)

        # make sure there are no skips in the topic numbers

        # convert frame_numbers in dictionary to time in video
        times_array = self.frame_number_to_time(self.dictionary_frame_text)
        print ('$' * 60)
        print (times_array)
        print ('$' * 60)

        # pass times as list to sub_clips.py
        Sub_Clip.create_subClips(self.video_dir, self.sub_clip_dir,times_array)

    # def passTimestoSubclips(self, times_array):
    #     sub_clips.subclip(times_array)

    def get_frame_rate(self,clip):
        moviepy_clip = VideoFileClip(clip)
        cap = cv2.VideoCapture(clip)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        clip_fps = length/moviepy_clip.duration 
        cap.release()
        del moviepy_clip
        del cap
        return clip_fps

    def frame_number_to_time(self, dictionary):
        times_array = list()
        for topic in dictionary:
            time = round(self.convert_frame_num_to_time( frame_number=dictionary[topic], frame_rate=self.frame_rate))
            times_array.append(time)
        return times_array

    def convert_frame_num_to_time(self, frame_number, frame_rate):
        return (frame_number/frame_rate)


    def orderDictionary(self, dictionary):
        ordered_dictionary = sorted(dictionary, key=dictionary.get, reverse=False)
        # for r in ordered_dictionary:
        #     print (str(r), str(ordered_dictionary[r]))
        return ordered_dictionary



    def getDictionary(self):
        return self.dictionary_frame_text


if __name__ == "__main__":
    cwd = os.getcwd()
    timings_class = GetTimings('small_video_tst_25s.mp4',cwd)
    timings_class.start() 