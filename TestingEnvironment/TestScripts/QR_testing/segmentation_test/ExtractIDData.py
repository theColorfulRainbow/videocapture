# This class will be an abstract get ID data class

class ExtractIDData(obj):

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
class ExtractIDDataQR(ExtractIDDate):

    # get the data by reading the frame and decoding it
    def _extract_data(self, frame):
        scanner = zbar.Scanner()
        results = scanner.scan(image)
        final_result = ""
        for result in results:
            result += result.data.decode('utf-8') + "\n"
        return final_result

# used to extract the code via text recognition using tesseract
# class ExtractIDDataTesseract(ExtractIDDate):
#
# # used to extract data using hamming and SIMM
# class ExtractIDDataHamming(ExtractIDDate):

def main():
    Extract_ID = ExtractIDDataQR()
    my_dir = os.getcwd()
    file_name = sys.argv[1]
    file_dir = os.path.join(my_dir,file_name)
    image = cv2.imread(file_dir, cv2.IMREAD_GRAYSCALE)
    print(Extract_ID.get_data(image))


if __name__=="__main__":
    main()
