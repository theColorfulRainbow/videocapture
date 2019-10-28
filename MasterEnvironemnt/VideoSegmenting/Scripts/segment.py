from Segmentor import Segmentor
import os
import sys
import time
# GOES BACK TWO times ("+ os.sep + os.pardir" x 2) and goes into Videos folder
VIDEO_DIRECTORY = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir + os.sep + os.pardir)
, "Videos")


def main():
    file_name = sys.argv[1]
    video_dir = os.path.join(VIDEO_DIRECTORY,file_name)
    sub_clip_dir = VIDEO_DIRECTORY

    my_Segmentor = Segmentor(video_dir,sub_clip_dir)
    

    my_Segmentor.start()

if (__name__ == "__main__"):
    main()
