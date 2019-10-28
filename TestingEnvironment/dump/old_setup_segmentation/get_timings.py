'''
Script deals with extracting the text from the frames that were extracted previously and the timeat which they occur
'''

from PIL import Image, ImageFont, ImageDraw
from pytesseract import image_to_string
import generate_frames
import datetime

# Given a frame returns the text from it
def get_frame_txt(frame):
    img_arr = Image.fromarray(frame)        # convert from array to image
    img_arr_grey = img_arr.convert('L')     # use grey converter (greyscale)
    
    img_arr_thresh = img_arr_grey.point(lambda x: 0 if 0<=x<=150 else 256) # set threshold for black and white 
    frame_txt = image_to_string(img_arr_thresh)                            # get text from black and white image
    return frame_txt


# -------------------Temporary-----------------------------------------
# List of uniques id's for end of topic
code_words = list()
for i in range(1,20):
    text = 'Topic nr.{} Signals and Communications 2'.format(str(i))
    code_words.append(text)
# ---------------------------------------------------------------------


frame_list = generate_frames.get_frames('small_video_tst_25s.mp4')
print('lenght of frame_list = ',len(frame_list))

topic_endings = list()

# counter iterating through topic list
counter_topic = 0
frame_counter = 1
# tigger for reaching end of topic
trig_end_topic = False
time_start = datetime.datetime.now()
fps = 29.97#cap.get(cv2.CAP_PROP_FPS)    # number of frames per second

for frame in frame_list:
    cur_frame_txt = get_frame_txt(frame)
    cur_video_time = str(datetime.timedelta(seconds=(frame_counter/fps)))
    print('-'*10,frame_counter,'-'*10,'\ntime: ',cur_video_time,'\nText:\n ',cur_frame_txt)
    frame_counter += 1
    print('\n',20*'_','\nCurent key phrase I am looking for:\n{}\nCurrent counter_topic = {}\n'.format(code_words[counter_topic],counter_topic),20*'_','\n')
    # check if end of current topic was reached
    if(code_words[counter_topic] in cur_frame_txt and trig_end_topic == False):
        trig_end_topic = True
        print('-'*10,frame_counter,'-'*10)
        print('\n',20*'*','\n','\nReached end of current topic\n','\n',20*'*','\n')
    # Check if you moved to the next topic
    if((code_words[counter_topic] in cur_frame_txt) == False and (trig_end_topic == True)):
        #increment counter to move to the next topic in the list 
        print('Counter BEFORE incrementing: {}'.format(counter_topic))
        counter_topic += 1
        print('Counter AFTER incrementing: {}'.format(counter_topic))
        trig_end_topic = False
        #record when new topic begins
        topic_endings.append(cur_video_time)
        print('\n',20*'*','\nMoved to the next topic\n','\n',20*'*','\n')
        print('Current time: {}'.format(cur_video_time))
time_end = datetime.datetime.now()
print('Time elapsed = {}'.format(str(time_end-time_start)))
print('topic_endings:\n {}'.format(topic_endings))