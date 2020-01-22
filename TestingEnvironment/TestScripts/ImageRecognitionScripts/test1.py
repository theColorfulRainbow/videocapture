# Script goes throught each video frame
# Scritps converts each frame to image
# Checks if each image contains uniques ID
# Records the time a new unique ID ismlast seen

#Necesary imports
import cv2
import os
from PIL import Image
import pytesseract

# working directorie and storing directory
video_dir = 'Desktop/Video_Capture/SignalsLecture.mp4'
store_dir = 'Desktop/Video_Capture/testFolder/'

# get the video as an object - vidcap
vidcap = cv2.VideoCapture(video_dir)

# Frame counter
count = 0
#need to set to true to get in the loop
success = True

# Loop that goes through every frame of the video
while success:
    success,image = vidcap.read()                           # check next frame

    if count%5==0:                                          # check only 5th frame
        cv2.imwrite(store_dir+"frame%d.jpg" % count, image) # save frame as JPEG file

    # text = pytesseract.image_to_string(Image.open(store_dir+"frame%d.jpg" % count))
    # print(text)

    print('Read a new frame: ', success)
    count += 1#                                             # increase frame counter
