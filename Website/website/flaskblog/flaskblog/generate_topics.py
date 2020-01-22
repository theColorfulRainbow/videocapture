'''
Scritps takes input from user: Name of subject and number of topics
Generates a folder of pdfs each containing the topics number
Generates a .zip file of the folder created
'''

import sys
import os
import flaskblog.generate_identifiers as generate_id
import zipfile
import shutil   # used to delete the stored topic numbers

TEMP_DIR = 'TopicsFile'
NUMBER_OF_TOPICS = 0
PNG_PDF_DIRECTORY = 'PNG_PDF_DIRECTORY'

def create_topic_zip_PDF(subject_name, number_of_topics, pdf_stored_dir):
    #global TEMP_DIR, NUMBER_OF_TOPICS
    #TEMP_DIR = 'TopicsFile'
    #NUMBER_OF_TOPICS = number_of_topics
    ## Create a folder to store code words
    #current_working_dir = os.getcwd()
    #print ('Current working directory: {}'.format(current_working_dir))
    #TEMP_DIR = '{} {}'.format(subject_name, TEMP_DIR)
    #temp_dir = TEMP_DIR
    #if not os.path.exists(temp_dir):
    #    print('Making Path')
    #    os.makedirs(temp_dir)

    # Need to ask user for the name of Subject & how many topics
    #subject_name = input('Please write the name of your subject and press Enter:\n')
    #print('you entered: {}'.format(subject_name))

    #number_of_topics = int(input('Please write how many topics you need:\n'))
    #print('you entered: {}'.format(number_of_topics))
    
    # delete the currently stored topics numbers
    #delete_stored_topics(temp_dir)
    # Generating a folder with the pdf code words
    #generatePDFList(subject_name,number_of_topics,temp_dir)
    # Generating the zip file

    global TEMP_DIR, NUMBER_OF_TOPICS
    NUMBER_OF_TOPICS = number_of_topics
    TEMP_DIR = pdf_stored_dir

    # check if the number of files inside the png id directory is smaller than than the number of topics,
    # if so then generate more PDF IDS
    for root, dirs, files in os.walk(TEMP_DIR):
        if (len(files) < number_of_topics):
            print('Topics Required: {}, Topics saved: {}, Generating new PDF Topics for {}'.format(number_of_topics,len(files),subject_name))
            generatePDFList(subject_name,number_of_topics,TEMP_DIR)

    generateZipFile(TEMP_DIR)

def create_topic_zip_PNG(subject_name, number_of_topics, png_stored_dir):
    global TEMP_DIR, NUMBER_OF_TOPICS
    NUMBER_OF_TOPICS = number_of_topics
    TEMP_DIR = png_stored_dir
    
    # check if the number of files inside the png id directory is smaller than than the number of topics,
    # if so then generate more PNG IDS
    for root, dirs, files in os.walk(TEMP_DIR):
        if (len(files) < number_of_topics):
            print('Topics Required: {}, Topics saved: {}, Generating new PNG Topics for {}'.format(number_of_topics,len(files),subject_name))
            generate_id_png(subject_name,number_of_topics,TEMP_DIR)

    generateZipFile(TEMP_DIR)

# creates both the PNG and PDF topics
def create_topic_zip_PNG_PDF(subject_name, number_of_topics, png_stored_dir, pdf_stored_dir):
    global TEMP_DIR, NUMBER_OF_TOPICS
    NUMBER_OF_TOPICS = number_of_topics
    TEMP_DIR = ('{} {}').format(subject_name,PNG_PDF_DIRECTORY)
    
    # check PNG has enough identifiers
    for root, dirs, files in os.walk(png_stored_dir):
        if (len(files) < number_of_topics):
            print('Topics Required: {}, Topics saved: {}, Generating new PNG Topics for {}'.format(number_of_topics,len(files),subject_name))
            generate_id_png(subject_name,number_of_topics,png_stored_dir)

    # check pdf has enough identifiers
    for root, dirs, files in os.walk(pdf_stored_dir):
        if (len(files) < number_of_topics):
            print('Topics Required: {}, Topics saved: {}, Generating new PDF Topics for {}'.format(number_of_topics,len(files),subject_name))
            generatePDFList(subject_name,number_of_topics,pdf_stored_dir)

    generateZipFilePNGPDF(TEMP_DIR,png_stored_dir,pdf_stored_dir)

'''
Deletes the stored topics in the current topic directory
'''
def delete_stored_topics(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

'''
Generate a list of pdfs in the directory CodeWordsTemp
'''
def generatePDFList(subject_name, number_of_topics,dir):
    code_words = list()
    subject_name_underscored = subject_name.replace(" ", "_")
    for i in range(1,number_of_topics+1):
        print(i)
        text = 'Topic nr.{}- Ended for {}. Any Questions?'.format(str(i),subject_name)
        filename = 'Topic_nr{}_{}'.format(str(i),subject_name_underscored)
        generate_id.createUniqueIdentifier(text,filename+'.pdf',dir)
        code_words.append(text)
    print('code_words:\n{}'.format(code_words))

def generate_id_png(subject_name, number_of_topics, dir):
    code_words = list()
    subject_name_underscored = subject_name.replace(" ", "_")
    for i in range(1,number_of_topics+1):
        print(i)
        # changed!, subject name will need to replace ' ' with '_' for easy integration on users side
        full_text = 'Topic nr.{}- Ended for {}. Any Questions?'.format(str(i),subject_name)
        filename = 'Topic_nr{}_{}'.format(str(i),subject_name_underscored)
        generate_id.createUniqueIdentifier(full_text,filename+'.png',dir)
        code_words.append(full_text)

    #list = ['Topic nr.','Ended for', 'Any Questions?']
    #topic_title = 'a'
    #bool ID = True
    #for string in list:
    #    if not(string in topic_title):
    #        ID = False
    #if (ID):
    #    # add to the dictionary

'''
Generate a zip file of the the folder with all code words
'''
def generateZipFile(dir):
    # now zipping the directory with all the pdfs
    print ('Zip files directory: {}'.format(dir))
    zipf = zipfile.ZipFile(str(dir)+'.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(dir,zipf)

def generateZipFileIntegratedPDF(dir):
    # now zipping the directory with all the pdfs
    print ('Zip files directory: {}'.format(dir))
    zipf = zipfile.ZipFile(str(dir)+'.zip', 'w', zipfile.ZIP_DEFLATED)
    zip(dir,zipf)

def generateZipFilePNGPDF(dir,png_dir,pdf_dir):
    print ('Zip files directory: {}'.format(dir))
    zipf = zipfile.ZipFile(str(dir)+'.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(png_dir,zipf)
    zipdir(pdf_dir,zipf)

'''
Function that deals with correct formatting of the .zip
'''
def zipdir(path, ziph):
    print('OS walk Path: {}'.format(os.walk(path)))
    # ziph is zipfile handle			
    for root, dirs, files in os.walk(path):
        # make sure to only zip the pdf files with the amount number included
        print('root: {}, dirs: {}, files: {}'.format(root, dirs, files))
        for file in files:
            print(file)
            # CHECK if the file contains a topic number wanted by the user
            for num in range(1,NUMBER_OF_TOPICS+1):
                print ('Number of topic: {}'.format(num))
                sub_string = '_nr{}_'.format(num) # this is needed so that if we only want the 1st topic pdf we dont also get all the other pds with 1 in them
                # like 10, 11, 21, 31 etc
                if (sub_string in file):
                    print ('Number is contained in file')
                    ziph.write(os.path.join(root, file))
                    break

                '''
Function that deals with correct formatting of the .zip
'''
def zip(path, ziph):
    print('OS walk Path: {}'.format(os.walk(path)))
    # ziph is zipfile handle			
    for root, dirs, files in os.walk(path):
        # make sure to only zip the pdf files with the amount number included
        print('root: {}, dirs: {}, files: {}'.format(root, dirs, files))
        for file in files:
            ziph.write(os.path.join(root, file))


def getTempDir():
    return TEMP_DIR

#def setTempDir():


if __name__ == "__main__":
    main()