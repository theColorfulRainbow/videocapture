'''
Script used to create a QR Image
'''
import pyqrcode
import sys

number_of_topics = int(sys.argv[1])

default = 'Topic nr.'
course_name = 'Signal and Communications 2'

for i in range(number_of_topics):
	message_final = default + str(i) + ' ' + course_name
	qr = pyqrcode.create(message_final)
	message_final_png = message_final+'.png'
	qr.png(message_final_png, scale=6)
