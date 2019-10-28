'''
Script/Class that creates threads and returns the frame (class) of video sequence
'''
# import the necessary packages
from threading import Thread
import sys
import cv2

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue

class FileVideoReadFrame:
    def __init__(self, path, id_extractor, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        # self.max_frame = 715 # int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        self.counter = 0
        # initialize the queue used to store frames read from the video file
        self.Q = Queue(maxsize=queueSize)
        self.frame_number = 0

    def start(self):
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
                print('Read Frames Thread Stopped')
                return
            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = self.stream.read()
                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stop()
                    return
                # add the frame to the queue
                self.Q.put(frame)
                self.counter += 1

    def read(self):
        # return next frame in the queue
        # need to make sure only 1 frame is giving to 1 thread and not more than 1 thread or else they
        # will converty the same text and thus waste time
        frame = self.Q.get()
        self.frame_number += 1
        # return self.Q.get()
        return [frame, self.frame_number]

    def get_time():
        # return the time of the current frame
        # doesn't work
        return self.Q.stream.get(cv2.CAP_PROP_POS_MSEC)

    def more(self):
        return (self.Q.qsize() > 0)

    def stop(self):
        # indicate that the thread should be stopped
        print('Initiaiting shutdown on read thread')
        self.stopped = True
