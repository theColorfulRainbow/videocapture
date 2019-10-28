'''
Script gets all necessary frames and puts them in a list
List of frames can then be used to extract the text 
'''
from FileVideoStream import FileVideoStream
from FileVideoStreamText import FileVideoRead
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2


from PIL import Image, ImageFont, ImageDraw
from pytesseract import image_to_string
import datetime

dictionary_frame_text = {}

def get_frame_txt(frame):
    img_arr = Image.fromarray(frame)        # convert from array to image
    img_arr_grey = img_arr.convert('L')     # use grey converter (greyscale)
    
    img_arr_thresh = img_arr_grey.point(lambda x: 0 if 0<=x<=150 else 256) # set threshold for black and white 
    frame_txt = image_to_string(img_arr_thresh)                            # get text from black and white image
    return frame_txt

def update_text_dictionary(text, frame_number):
    if text in dictionary_frame_text:
        saved_frame_number = dictionary_frame_text[text]
        if saved_frame_number < frame_number: 
            dictionary_frame_text[text] = frame_number
    else:
        dictionary_frame_text[text] = frame_number


args = 'small_video_tst_25s.mp4'

print("[INFO] starting video file thread...")
fvs = FileVideoStream(args).start()
time.sleep(1.0)
frame_list = list()
# start the FPS timer
fps = FPS().start()

# initialising the threads for getting the text from frames
for i in range(10):
    fvr = FileVideoRead(fvs,i,'hello').start()

# loop over frames from the video file stream
while fvs.more():
        frame, frame_number = fvs.read() #get frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])    
        main_thread_frame_txt = get_frame_txt(frame)
        print('frame_number = {}\ncur_frame_txt:\n{}'.format(frame_number,main_thread_frame_txt))
        fps.update()
    
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()
print('lenght of frame_list = ',len(frame_list))


#-------------------------------------------------------------------------
# import cv2
# import time
# vidcap = cv2.VideoCapture('small_video_tst_25s.mp4')
# success,frame = vidcap.read()
# count = 0

# frame_list = list()
# start = time.time()
# while success:
#     # frame_list.append(frame)
#     # time.sleep(0.1)
#     # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
#     success,frame = vidcap.read()
#     # print('Read a new frame: ', success)
#     count += 1
#     # if count % 200:
#     #     collectgarbage()
#     print(count)
# end = time.time()
# print('len(frame_list)',len(frame_list))
# print((end - start).total_seconds())

#-------------------------------------------------------------------------

# import cv2
# from skimage.io import Video
# import sys
# print(sys.path)

# cap = Video('small_video_tst_25s.mp4')
# fc = cap.frame_count()
# for i in np.arange(fc):
#    z = cap.get_index_frame(i)


