# This file will deal with breaking
# up the video into frames and saving those
# frames as png files

## TESTED and Working 20/12/18

import os
import math
from moviepy.editor import *

# code taken from https://stackoverflow.com/questions/43148590/extract-images-using-opencv-and-python-or-moviepy
# assume times array has the end time for the clip since we will not have
# an identifier in the last slide
def create_subClips(movie,destination_directory,times_array,course_name):
    # load information about clip to variables
    clip = VideoFileClip(movie)
    # check that last element in times array is within video duration
    if(times_array[-1]>clip.duration):
        times_array[-1] = int(math.floor(clip.duration)) 
    print('clip_duration={}\ntimes_array={}'.format(clip.duration,times_array))
    # define variable for when to start the clip to where to end it
    last_time = 0
    # create sub clips array
    sub_clip_array = []
    # create sub clips and save them to the sub_clip_array
    for time in times_array:
        sub_clip = clip.subclip(last_time, time)
        sub_clip_array.append(sub_clip)
        last_time = time    
    # save the sub clips to a directory 
    for i in range(len(sub_clip_array)):
        name = "{}\{}-Topic#{}.mp4".format(destination_directory,course_name,i)
        print(name)
        sub_clip_array[i].write_videofile(name)
    
