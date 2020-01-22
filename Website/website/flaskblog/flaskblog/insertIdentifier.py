## this file deals with inserting the template in
## positions of the pdf

### Works 20/12/18

# this file deals with inserting the template in
# positions of the pdf

## Works 20/12/18

from PyPDF2 import PdfFileReader, PdfFileWriter
import os

UNIQUE_PDF_ID = 'pdf_with_Unique_ID.pdf'
UNIQUE_PPTX_ID = 'pptx_with_unique_id.pptx'

def insert_Identifier(PDF,des_directory,positions_array, identifier_array):
    # initilaise pdf variables
    full_pdf = PdfFileReader(open(r"{}".format(PDF), "rb"))
    saved_page_number = 0
    new_pdf = PdfFileWriter()   
    total_page_num = full_pdf.getNumPages() # get how many pages pdf has
    print('PDF = {}, des directory = {}'.format(PDF,des_directory))
    
    #if last page has ending => all good; else => insret manualy
    if(not(total_page_num in positions_array)):
        positions_array.append(total_page_num+1)
    
    # create unique id array
    #identifier_array = []
    #for i in range(1,len(positions_array)+1):
    #    filename = 'id_folder\\pdfs\\Topic nr.{} Signals and Communications 2.pdf'.format(str(i))
    #    identifier_pdf = PdfFileReader(open(r"{}".format(filename), "rb"))
    #    print(filename)
    #    identifier_array.append(identifier_pdf)

    # check that the positions array = identifier array length
    if (not checks_PDF(PDF,des_directory,positions_array,identifier_array)):
        print("Positions array length = {}\nIdentifier Array Lenght = {}".format(len(positions_array),len(identifier_array)))
        return
    
    # loop over PDF and insert identifier in slots
    for i in range(len(positions_array)):
        page_position = positions_array[i]
        # copy apporpriate pdfs before where identifier is to be placed
        while (saved_page_number < page_position):
            new_pdf.addPage(full_pdf.getPage(saved_page_number))
            saved_page_number += 1
        # after copying all the appropriate pdfs, now add in the identifier
        new_pdf.addPage((identifier_array[i].getPage(0)))
        
    # name of pdf file to be saved
    pdf_name = os.path.join(des_directory,'pdf_with_Unique_ID.pdf')

    # write pdf file to specified location with specified name
    outputStream = open(pdf_name, "wb")
    new_pdf.write(outputStream)
    outputStream.close()

        
# this will perform checks to see if the proccess is possible 
def checks_PDF(PDF,des_directory,positions_array,identifier_array):
    if ( not (len(positions_array) == len(identifier_array))):
        print("Positions array length = {}\nIdentifier Array Lenght = {}".format(len(positions_array),len(identifier_array)))
        print("Positions array and Identifier Array not equal Length!")
        return False
    for num in positions_array:
        print ('Number = {}, Total Page number = {}'.format(num,get_total_page_number(PDF)))
        if (num > get_total_page_number(PDF)):
            print ('RETURING FALSE!!!!!!!!!!!!!!!')
            return False
    return True

# this will perform checks to see if the proccess is possible 
def checks_PPTX(positions_array,identifier_array, total_slides):
    if ( not (len(positions_array) == len(identifier_array))):
        print("Positions array length = {}\nIdentifier Array Lenght = {}".format(len(positions_array),len(identifier_array)))
        print("Positions array and Identifier Array not equal Length!")
        return False
    for num in positions_array:
        print ('Number = {}, Total Page number = {}'.format(num,total_slides))
        if (num > total_slides):
            print ('RETURING FALSE!!!!!!!!!!!!!!!')
            return False
    return True

def get_identifier_list_from_pdf(filenames):
    identifier_list = []
    for name in filenames:
        identifier_list.append(get_identifier_from_pdf(name))
    return identifier_list

# filename_list is a list of filenames in string format e.g ['sig and coms 1', 'sigs and coms 2'] 
def get_identifier_from_pdf(filename):
    # create identifier pdf
    identifier_pdf = PdfFileReader(open(r"{}".format(filename), "rb"))
    return identifier_pdf

def get_total_page_number(pdf):
    full_pdf = PdfFileReader(open(r"{}".format(pdf), "rb"))
    total_page_num = full_pdf.getNumPages() # get how many pages pdf has
    return total_page_num