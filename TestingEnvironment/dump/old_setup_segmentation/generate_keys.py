'''
Scritps takes input from user: Name of subject and number of topics
Generates a folder of pdfs each containing the topics number
Generates a .zip file of the folder created
'''

import sys
import os
import generate_keys_pdf as mkPFD
import zipfile


def main():
	# Create a folder to store code words
	current_working_dir = os.getcwd()
	temp_dir = 'CodeWordsTemp'
	if not os.path.exists(temp_dir):
	    os.makedirs(temp_dir)

	# Need to ask user for the name of Subject & how many topics
	subject_name = input('Please write the name of your subject and press Enter:\n')
	print('you entered: {}'.format(subject_name))

	number_of_topics = int(input('Please write how many topics you need:\n'))
	print('you entered: {}'.format(number_of_topics))

	# Generating a folder with the pdf code words
	generatePDFList(subject_name,number_of_topics,temp_dir)
	# Generating the zip file 
	generateZipFile(temp_dir)

'''
Generate a list of pdfs in the directory CodeWordsTemp
'''
def generatePDFList(subject_name, number_of_topics,dir):
	code_words = list()
	for i in range(1,number_of_topics+1):
		print(i)
		text = 'Topic nr.{}- {}'.format(str(i),subject_name)
		mkPFD.createUniqueIdentifier(text,text+'.pdf',dir)
		code_words.append(text)
	print('code_words:\n{}'.format(code_words))


'''
Generate a zip file of the the folder with all code words
'''
def generateZipFile(dir):
	# now zipping the directory with all the pdfs
	zipf = zipfile.ZipFile(str(dir)+'.zip', 'w', zipfile.ZIP_DEFLATED)
	zipdir(dir,zipf)

'''
Function that deals with correct formatting of the .zip
'''
def zipdir(path, ziph):
    # ziph is zipfile handle			
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


if __name__ == "__main__":
    main()