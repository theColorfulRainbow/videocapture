'''
Test script used as example of how to decode QR
'''

import cv2
import os
import numpy as np
import zbar
import sys

my_dir = os.getcwd()
file_name = sys.argv[1]

file_dir = os.path.join(my_dir,file_name)

image = cv2.imread(file_dir, cv2.IMREAD_GRAYSCALE)
scanner = zbar.Scanner()
results = scanner.scan(image)
for result in results:
    print((result.data.decode('utf-8')))
