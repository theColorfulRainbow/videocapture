import os
import gc
import cv2
import sys
import time
import scipy
import itertools
import numpy as np
import matplotlib.pyplot as plt
from imageio import imread, imwrite 
from skimage.transform import resize
from skimage.measure import compare_ssim
# from io import BytesIO


class ImageComparer(object):

	def __init__(self, id_directory):
		self.ID_DIRECTORY = id_directory
		self.init_id_dictionary()
		self._print_function()
		# we want the same size as the frame which is (720,1280)
		self.SIZE = (int(1280), int(720))
		self.init_image_list()
		self.TOP_LEFT_BORDER = []
		self.BOTTEM_RIGHT_BORDER = []
	
	# initialise dictionary that links topic numbers to difference scores
	def init_id_dictionary(self):
		image_titles = os.listdir(self.ID_DIRECTORY)
		images_correct_format = self._filter_images(image_titles) 
		if (images_correct_format==True):
			self.TITLE_TO_DIFFERENCE_DICT = {}
			for title in image_titles:
				score = self._difference_score(title,height=30,width=30)
				self.TITLE_TO_DIFFERENCE_DICT[title] = score 
				print('{} correctly added'.format(title))
		else:
			print('ERROR: IMAGES NOT IN CORRECT FORMAT\nEXITING...')
			exit()

	def init_image_list(self):
		image_titles = os.listdir(self.ID_DIRECTORY)
		# list conatining CV2 imread ogf all IDS
		cv2_images = {}
		for title in image_titles:
			print(os.path.join(self.ID_DIRECTORY,title))
			image = cv2.imread(os.path.join(self.ID_DIRECTORY,title))
			image = cv2.resize(image, self.SIZE)
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cv2_images[title] = image
			print('Image Shape for {}: {}'.format(title, image.shape))
		self.CV2_IMAGES = cv2_images

	# will return true if this frame is very similar to the saved border framed ID's
	def is_topic_slide(self,frame):
		frame_format = self._filter_frame(frame)
		if (frame_format==True):	# check if correct format first 
			score = self._difference_score_frame(frame, height = 30, width = 30) # cehck if inside dictionary
			title = self._get_dupliacte_image(score)
			if (title == ''):
				return False
			else:
				return True


	# returns topic number if image in dictionary or not
	def get_topic_number(self, frame):
		frame_format = self._filter_frame(frame)
		if (frame_format==True):	# check if correct format first 
			score = self._difference_score_frame(frame, height = 30, width = 30) # cehck if inside dictionary
			# get the title of the matching image
			title = self._get_dupliacte_image(score)
			# check the title is valid
			if (title != ''):
				# topic_number = self._get_topic_number_from_title(title)
				return True
			else:
				return False
		else:
			print('ERROR: frame GIVEN NOT IN CORRECT FORMAT\nEXITING...')
			exit()
		os.remove()
	#---------------------------------------------------------------------
	#                        HELPER FUNCTIONS 
	#---------------------------------------------------------------------

	# return the difference score given an IMAGE directory
	def _difference_score(self, image, height = 30, width = 30):
	    gray = self._img_gray(image)
	    row_res, col_res = self._resize(gray, height, width)
	    difference = self._intensity_diff(row_res, col_res)
	    return difference


    # return the difference score given a FRAME
	def _difference_score_frame(self, frame_jpg, height = 30, width = 30):
		try:
			gray = np.average(frame_jpg, weights=[0.299, 0.587, 0.114], axis=2)
			row_res, col_res = self._resize(gray, height, width)
			difference = self._intensity_diff(row_res, col_res)
		except:
			gc.collect()
			time.sleep(1)
			gray = np.average(frame_jpg, weights=[0.299, 0.587, 0.114], axis=2)
			row_res, col_res = self._resize(gray, height, width)
			difference = self._intensity_diff(row_res, col_res)
		return difference


	# Return True/False if image is correct format
	def _filter_frame(self, frame):
		return (frame.shape[2]==3)


	# Returns True/False if lsit of images are correct format
	def _filter_images(self, images):
		for image in images: 
			try:
				image = os.path.join(self.ID_DIRECTORY,image)
				# print('imread(image).shape = {}'.format(imread(image).shape))
				# print('IMAGE: {}'.format(image))
				assert imread(image).shape[2] == 3
			except  AssertionError as e:
				print('IMAGE: {}\nERROR:\n'.format(image,e))
				return False
		return True

	#First turn the image into a gray scale image
	def _img_gray(self, image):
		im = os.path.join(self.ID_DIRECTORY,image)
		image = imread(im)
		self.AVERAGE = np.average(image, weights=[0.299, 0.587, 0.114], axis=2)
		return self.AVERAGE

    #resize image and flatten
	def _resize(self, image, height=30, width=30):
	    row_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten()
	    col_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten('F')
	    return row_res, col_res



	#gradient direction based on intensity 
	def _intensity_diff(self, row_res, col_res):
	    difference_row = np.diff(row_res)
	    difference_col = np.diff(col_res)
	    difference_row = difference_row > 0
	    difference_col = difference_col > 0
	    return np.vstack((difference_row, difference_col)).flatten()


	#Hamming distance
	def _hamming_distance(self, image, image2):
	    score = scipy.spatial.distance.hamming(image, image2)
	    return score

	# returns the title of an image if it matches the frame
	def _get_dupliacte_image(self, score):
		smallest_difference = 1.0
		estimated_title = ''
		for title in self.TITLE_TO_DIFFERENCE_DICT:
			image = self.TITLE_TO_DIFFERENCE_DICT[title]
			# print('shape of frame: {}, shape of image:{}'.format(frame.shape, image.shape))
			difference = self._hamming_distance(image, score)
			# print('Hamming Difference: {}'.format(difference))
			if (difference < smallest_difference and difference < 0.24):
				estimated_title = title
				smallest_difference = difference
			# if self._hamming_distance(image, frame) < .10:	# return duplicate image
			#     return title
		# print('Hamming stats:\nsmallest_difference = {}, estimated title: {}'.format(smallest_difference, estimated_title))
		return estimated_title

	# returns the topic number from title of topic 
	def _get_topic_number_from_title(self, title):
		start_idx = 9	# start looking after '.' from Topic nr.{}-
		title_len = len(title)
		current_idx = start_idx
		number_str = ''
		while(current_idx < title_len):
			current_char = title[current_idx]
			if (current_char.isdigit()):
				number_str += current_char
				current_idx += 1
			else:
				break
		return int(number_str)

	# assume frame is already greyscaLed
	def get_SSIM_topic_number(self, frame):
		biggest_score = -1.0
		estimated_title = ''
		for title in self.CV2_IMAGES:
			image = self.CV2_IMAGES[title]
			score = self.SSIM_compare(image, frame)
			if (score > biggest_score and score > 0.85):
				estimated_title = title
				biggest_score = score
		print('biggest score = {}, estimated title: {}, last score: {}'.format(biggest_score, estimated_title, score))
		return estimated_title

	def SSIM_compare(self, image_1, bordeless_frame):
		bordeless_frame = cv2.cvtColor(bordeless_frame, cv2.COLOR_BGR2GRAY)
		bordeless_size = bordeless_frame.shape
		if not(bordeless_size > (400,500)):
			return -1
		# compute the Structural Similarity Index (SSIM) between the two
		# images, ensuring that the difference image is returned
		(score, diff) = compare_ssim(image_1, bordeless_frame, full=True)
		diff = (diff * 255).astype("uint8")
		return score
	
	def get_border_cut_image(self,image):
		frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		bordeless_frame, top_left_indice, bottem_right_indice = self.cut_border(frame)
		return bordeless_frame, top_left_indice, bottem_right_indice

	def cut_border(self, image):
		indices = (np.argwhere(image>10))
		if (self.TOP_LEFT_BORDER == [] or self.BOTTEM_RIGHT_BORDER == []):
			top_left_indice = indices[0]
			bottem_right_indice = [self.SIZE[1] - top_left_indice[0], self.SIZE[0] - top_left_indice[1]]
		else:
			top_left_indice = self.TOP_LEFT_BORDER
			bottem_right_indice = self.BOTTEM_RIGHT_BORDER

		image_without_border = image[top_left_indice[0]:bottem_right_indice[0],top_left_indice[1]:bottem_right_indice[1] ]
		return image_without_border, top_left_indice, bottem_right_indice

	#---------------------------------------------------------------------
	#                        	DEBUGGING
	#---------------------------------------------------------------------

	def _print_function(self):
		print('DICTIONARY : \n{}'.format(self.TITLE_TO_DIFFERENCE_DICT))
