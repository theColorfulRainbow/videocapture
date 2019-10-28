# This file will deal with breaking
# up the video into frames and saving those
# frames as png files

## TESTED and Working 20/12/18

import os
from moviepy.editor import *

# code taken from https://stackoverflow.com/questions/43148590/extract-images-using-opencv-and-python-or-moviepy
# assume times array has the end time for the clip since we will not have
# an identifier in the last slide
def create_subClips(movie,destination_directory,times_array):
    # load information about clip to variables
    clip = VideoFileClip(movie)
    fps = clip.fps
    # define variable for when to start the clip to where to end it
    last_time = 0
    # create sub clips array
    sub_clip_array = []
    
    # create sub clips and save them to the sub_clip_array
    for time in times_array:
        sub_clip = clip.subclip(last_time, time)
        sub_clip_array.append(sub_clip)
        last_time = time
        
    # save the sub clips to a directory (may later be merged with creation
    # of sub clips loop)
    for i in range(len(sub_clip_array)):
        name = "{}\Test Clip #{}.mp4".format(destination_directory,i)
        print(name)
        sub_clip_array[i].write_videofile(name)
    
