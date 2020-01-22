# This script creates the unique identifier
import sys
import zipfile
from PIL import Image,ImageFont,ImageDraw

# should be used when you want to save the unique identifier  
def createUniqueIdentifier(text,filename,save_directory):
    '''
        DEFINITION:
            Creates a pdf with given text & saves it to given directory
        INPUT:
            text - text that will be saved on the pdf
            filename - name of the file saved
            save_directory - directory that pdf will be saved
    '''
    # create the image with a white background
    img_width = 1920
    img_height = 1080
    img = Image.new('RGB',(img_width,img_height),'white')
    # set the font of the text to basic arial and get the correct 
    # fontsize so the text can all fit into the image
    fontsize = getFontSize(img_width,img_height,text)
    font = ImageFont.truetype('arial.ttf',fontsize)
    # get the width and height of the font
    width,height = font.getsize(text)
    # draw the text on the screen
    draw = ImageDraw.Draw(img)
    sizes = ((img_width-width)/2, (img_height-height)/2)
    draw.text(sizes, text, font=font,fill='black')

    # display the image
    # img.show()
    print('!'*10)
    print(save_directory)
    print(filename)
    print('!'*10)
    # save the image
    img.save(save_directory+'\\'+filename)
 
# used for debugging    
def main():
    text = sys.argv[1]
    for i in range(1,20):
        text = 'Topic nr.{} Signals and Communications 2'.format(str(i))
        save_dir = 'id_folder\\pdfs'
        createUniqueIdentifier(text,filename=text+'.pdf',save_directory=save_dir)

# gets the correct font size for the text to be fully displayed in the image,
# should be used for getting optomised fontsize
def getFontSize(image_width,image_height, text):
    fontsize = 1  # starting font size
    # portion of image width you want text width to be
    blank = Image.new('RGB',(image_width, image_height))
    font = ImageFont.truetype("arial.ttf", fontsize)
    
    while (font.getsize(text)[0] < blank.size[0]) and (font.getsize(text)[1] < blank.size[1]):
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype("arial.ttf", fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    return fontsize


# if __name__ == "__main__":
#         main()