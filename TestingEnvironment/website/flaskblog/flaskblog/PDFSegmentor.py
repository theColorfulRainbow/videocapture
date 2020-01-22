# This file will copy all pages of a pdf file to a new pdf
# file given an array with page numbers starting at 0.
# It will not copy the page which has the corresopnding
# page number of one in the positions array
# if you want to copy the first two pages then make
# sure the positions_array contains 2. It will not copy the 2nd page
# indenting from 0, or as viewed from pdf viewer page number 3

# Tested and working 20/12/18

from PyPDF2 import PdfFileReader, PdfFileWriter
import os
# this method segmants the pdf depending on the page numbers in the
# positions array. Assumes it will contain the last page number
# for complete segmentation
def segment_PDF(PDF,des_directory,positions_array):
    # new segmented pdf

    seg_pdf = PdfFileWriter()
    # full pdf (assume 'r' has been added before)
    full_pdf = PdfFileReader(open(r"{}".format(PDF), "rb"))


    # print how many pages input1 has:
    #print("full pdf has %d pages." % full_pdf.getNumPages())

    # array that stores the position
    # of every slide where our marker has appeared
    #positions_array = [3,5]

    # if we want dont plan on having a mark at the end
    # then just add the total page length so it will crop properly
    #positions_array.insert(len(positions_array),full_pdf.getNumPages())

    saved_page_number = 0
    counter = 0
    for i in range(len(positions_array)):
        seg_pdf = PdfFileWriter()
        page_position = positions_array[i]
        print('pos before while loop{}'.format(str(page_position)))
        while (saved_page_number < (page_position)):
            print('Page {} getting added'.format(str(saved_page_number)))
            seg_pdf.addPage(full_pdf.getPage(saved_page_number+counter))
            saved_page_number += 1
        counter += 1

        # name of pdf file to be saved
        name = "Topic {}.pdf".format(i)
        pdf_name = os.path.join(des_directory,name)
        # write pdf file to specified location with specified name
        outputStream = open(pdf_name, "wb")
        seg_pdf.write(outputStream)
        outputStream.close()