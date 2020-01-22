# This class will be an abstract get ID data class

class ExtractIDData(object):

    def __init__(self):
        self.data = "";

    # call this method to get the data associated with the frame in string type
    def get_data(self, frame):
        self.data = self._extract_data(frame)
        return self.data

    # extract the data depending on the specific way we are using it
    def _extract_data(self, frame):
        pass

import cv2
import os
import numpy as np
import zbar
import sys

# used to extarct the data via qr code
class ExtractIDDataQR(ExtractIDData):

    def __init__(self):
        ExtractIDData.__init__(self)
        self.scanner = zbar.Scanner()

    # get the data by reading the frame and decoding it
    def _extract_data(self, frame):
        results = self.scanner.scan(frame)
        final_result = ""
        for result in results:
            final_result += str(result.data.decode('utf-8'))
        return final_result

# used to extract the code via text recognition using tesseract
class ExtractIDDataTesseract(ExtractIDDate):
    def __init__(self):
        ExtractIDData.__init__(self)
        self.TEXT_ID_LIST = ['Topic nr.','Topic --']

    def _extract_data(frame):
        img_arr = Image.fromarray(frame)        # convert from array to image
        img_arr_grey = img_arr.convert('L')  # use grey converter (greyscale)
        img_arr_thresh = img_arr_grey.point(lambda x: 0 if 0<=x<=150 else -256) # set threshold for black and white
        frame_txt = image_to_string(img_arr_thresh) # get text from black and white image
        return frame_txt

#
# # used to extract data using hamming and SIMM
class ExtractIDDataHamming(ExtractIDDate):

    def _extract_data(frame):
        img_arr = Image.fromarray(frame)        # convert from array to image
        img_arr_grey = img_arr.convert('L')  # use grey converter (greyscale)
        img_arr_thresh = img_arr_grey.point(lambda x: 0 if 0<=x<=150 else -256) # set threshold for black and white
        frame_txt = image_to_string(img_arr_thresh) # get text from black and white image
        return frame_txt

def main():
    Extract_ID = ExtractIDDataQR()
    my_dir = os.getcwd()
    file_name = sys.argv[1]
    file_dir = os.path.join(my_dir,file_name)
    image = cv2.imread(file_dir, cv2.IMREAD_GRAYSCALE)
    print(Extract_ID.get_data(image))


if __name__=="__main__":
    main()
