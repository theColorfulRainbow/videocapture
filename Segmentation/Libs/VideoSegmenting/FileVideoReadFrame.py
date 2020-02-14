'''
Script/Class that creates threads and returns the frame (class) of video sequence
'''
# import the necessary packages
from threading import Thread
import sys
import cv2
# import MasterEnvironemnt.Logger 
import logging
from queue import Queue

class FileVideoReadFrame(object):
    def __init__(self, path, id_extractor, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.logger = logging.getLogger("Logger")
        self.stream = cv2.VideoCapture(path)
        self.logger.debug('path={}'.format(path))
        self.stopped = False
        # self.max_frame = 715 # int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.counter = 0
        # initialize the queue used to store frames read from the video file
        self.Q = Queue(maxsize=queueSize)
        self.q_size = queueSize
        self.frame_number = 0
        self.started = False

    def start(self):
        self.logger.info('started reading frames...')
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                # print('Read Frames Thread Stopped')
                return
            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()
                # print('FRAME WAS GRABBED: ')
                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    #self.logger.info("Frame could not be grabbed. exiting Read Frame, total frames read: {}".format(self.counter))
                    self.stop()
                    return
                # add the frame to the queue
                self.Q.put(frame)
                self.counter += 1
                self.started=True
            # print("Frame Not Grabbed, Q size: {}".format(self.Q.qsize()))

    def read(self):
        # return next frame in the queue
        # need to make sure only 1 frame is giving to 1 thread and not more than 1 thread or else they
        # will converty the same text and thus waste time
        frame = self.Q.get()
        self.frame_number += 1
        # return self.Q.get()
        return [frame, self.frame_number]

    def more(self):
        return (self.Q.qsize() > 0)

    def stop(self):
        # indicate that the thread should be stopped
        self.logger.info('Initiaiting shutdown on read thread')
        self.stopped = True
