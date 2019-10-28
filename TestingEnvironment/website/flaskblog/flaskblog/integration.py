# This file contains fucntions for integrating and downloading the files for the website

# -- Imports --
from flaskblog.insertIdentifier import insert_Identifier, get_identifier_list_from_pdf, get_total_page_number, UNIQUE_PDF_ID,UNIQUE_PPTX_ID,checks_PDF, checks_PPTX
import os
import secrets
from flaskblog.powerpoint import Powerpoint

# -- CONSTANTS --
ROOT_DIRECTORY = os.getcwd()

UPLOADED_PDF_DIRECROTY = os.path.join(ROOT_DIRECTORY,'Uploaded_PDF')
UPLOADED_PPTX_DIRECROTY = os.path.join(ROOT_DIRECTORY,'Uploaded_PPTX')

SEGMENTED_PDF_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Segmented_PDF')

INTEGRATED_PDF_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Integrated_PDF')
INTEGRATED_PPTX_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Integrated_PPTX')

IDENTIFIER_PNG_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Identifier_PNG')
IDENTIFIER_PDF_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Identifier_PDF')

# -- Methods --

# used to save the PDF or Powerpoint slide they have uploaded
def save_PDF(form_pdf):
    # give random name so it doesn not overwrite other stored PDF
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pdf.filename)  # get the correct file extension
    pdf_filename = random_hex + f_ext   # create unique filename
    pdf_path_name = os.path.join(UPLOADED_PDF_DIRECROTY, pdf_filename)
    form_pdf.save(pdf_path_name)

    return pdf_path_name

# save a powerpoint file given by the user
def save_pptx(form_pptx):
    # give random name so it doesn not overwrite other stored PDF
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pptx.filename)  # get the correct file extension
    pptx_filename = random_hex + f_ext   # create unique filename
    pptx_path_name = os.path.join(UPLOADED_PPTX_DIRECROTY, pptx_filename)
    form_pptx.save(pptx_path_name)

    return pptx_path_name


# checks if the page numbers provided are valid
def is_valid_topics(topic_string):
    try:
        # remove all whitespace
        topic_string = topic_string.replace(" ", "")
        print (topic_string)
        # make sure it goes: 1 number then 1 comma
        topic_list = [int(s) for s in topic_string.split(',')]
        print (topic_string)
        print ('Sorted List: {}'.format(sorted(topic_list)))
        # check topic_list is in ascending order
        if not(topic_list == sorted(topic_list)):
            return False
        # check all
        return True
    except:
        return False


# converts the raw page numbers into a list
def convert_topics_to_list(topic_string):
    # remove all whitespace
    topic_string = topic_string.replace(" ", "")
    print (topic_string)
    # make sure it goes: 1 number then 1 comma
    topic_list = [int(s) for s in topic_string.split(',')]
    print (topic_string)
    return topic_list


# gets the pdf files of the unique identifier and stores them into an array as PDF objects
def get_pdf_object(course_name, number_of_topics):
    pdf_dir = os.path.join(IDENTIFIER_PDF_DIRECTORY,course_name)
    file_names = []
    for root, path, files in os.walk(pdf_dir):
        for num in range(1,number_of_topics + 1):
            for file in files:
                sub_string = '_nr{}_'.format(num) # this is needed so that if we only want the 1st topic pdf   we dont also get all the other pds with 1 in them
                #print (sub_string + ' hehehe' )
                # like 10, 11, 21, 31 etc
                if (sub_string in file):
                    print (file)
                    file_names.append(os.path.join(root, file))
                    break
    print ('Filenames: {}, pdf_directory where these pdf filenames come from: {}'.format(file_names,pdf_dir))

    # now get the unique identifier array
    identifier_array = get_identifier_list_from_pdf(file_names)
    print(identifier_array)
    return identifier_array


# gets the Unique Idenitifers png files
def get_id_paths(course_name, number_of_topics):
    id_dir = os.path.join(IDENTIFIER_PNG_DIRECTORY,course_name)
    file_names = []
    for root, path, files in os.walk(id_dir):
        for num in range(1,number_of_topics + 1):
            for file in files:
                sub_string = '_nr{}_'.format(num) # this is needed so that if we only want the 1st topic pdf   we dont also get all the other pds with 1 in them
                print (sub_string + ' hehehe' )
                # like 10, 11, 21, 31 etc
                if (sub_string in file):
                    print ('FILE NAME IN GET_ID_PATHS = ' + str(file))
                    file_names.append(os.path.join(root, file))
                    break
    print ('Filenames: {}, ID_directory where these png filenames come from: {}'.format(file_names,id_dir))
    return file_names


# integrates the ID into the powerpoint slide provided by the user
def pptx(pptx_form, topic_list, course_1):
    pptx_path_name = save_pptx(pptx_form)
    save_name = UNIQUE_PPTX_ID
    PowerPoint = Powerpoint(pptx_path_name, INTEGRATED_PPTX_DIRECTORY, save_name)
    total_slides = PowerPoint.get_total_slides()

    if not (total_slides in topic_list):
        print('Total powerpoint slides: {}, and its not in the slide_numbers thus adding now'.format(total_slides))
        topic_list.append(total_slides)

    # get the paths to the identifier png files
    id_path = os.path.join(IDENTIFIER_PNG_DIRECTORY,course_1)
    id_array = get_id_paths(course_1, len(topic_list))
    
    print('In PPTX, Topic list = {}, ID_array = {}'.format(topic_list,id_array))
    # increment the topic numbers by 1
    insert_slide_positions = [x+1 for x in topic_list]

    # insert the id into the slides

    if (checks_PPTX(topic_list, id_array, total_slides)):
        PowerPoint.add_images(insert_slide_positions, id_array)
        PowerPoint.save_pptx(save_name)
        return True
    else:
        return False


# integrates the ID into the PDF slide provided by the user
def pdf(pdf_form, topic_list, course_1):
    pdf_path_name = save_PDF(pdf_form)
                    
    if (not (get_total_page_number(pdf_path_name) in topic_list)):
        topic_list.append(get_total_page_number(pdf_path_name))
        print(get_total_page_number(pdf_path_name))

    identifier_array = get_pdf_object(course_1, len(topic_list))
    des_dir = INTEGRATED_PDF_DIRECTORY

    print ('Positions array = {}, identifier_array = {}'.format(topic_list, identifier_array))
    if (checks_PDF(pdf_path_name,des_dir,topic_list,identifier_array)):
        insert_Identifier(pdf_path_name,des_dir,topic_list,identifier_array)
        return True
    else:
        return False