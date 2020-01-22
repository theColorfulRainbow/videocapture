'''
Script used to create a QR Image
'''
import pyqrcode
import sys

message = sys.argv[1]
message_filename = message+'.png'

qr = pyqrcode.create(message)
qr.png(message_filename, scale=6)
