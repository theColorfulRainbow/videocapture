# -- Imports --
from flask import render_template, url_for, flash, redirect, send_file, request
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm, LectureForm, PDFUpload, LectureUpload
from flaskblog.models import User, Post
from flaskblog.generate_topics import create_topic_zip_PNG, create_topic_zip_PDF , getTempDir, generate_id_png, generateZipFileIntegratedPDF, delete_stored_topics, create_topic_zip_PNG_PDF
import os
from flaskblog.insertIdentifier import insert_Identifier, get_identifier_list_from_pdf, get_total_page_number, UNIQUE_PDF_ID,UNIQUE_PPTX_ID,checks_PDF, checks_PPTX
import pathlib
from flaskblog.generate_identifiers import createUniqueIdentifier
import secrets
from flaskblog.PDFSegmentor import segment_PDF
from flaskblog.integration import save_PDF, save_pptx, is_valid_topics, convert_topics_to_list, get_pdf_object, get_id_paths, pptx, pdf

# -- CONSTANTS --
ROOT_DIRECTORY = os.getcwd()

UPLOADED_PDF_DIRECROTY = os.path.join(ROOT_DIRECTORY,'Uploaded_PDF')
UPLOADED_PPTX_DIRECROTY = os.path.join(ROOT_DIRECTORY,'Uploaded_PPTX')

SEGMENTED_PDF_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Segmented_PDF')

INTEGRATED_PDF_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Integrated_PDF')
INTEGRATED_PPTX_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Integrated_PPTX')

IDENTIFIER_PNG_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Identifier_PNG')
IDENTIFIER_PDF_DIRECTORY = os.path.join(ROOT_DIRECTORY,'Identifier_PDF')

EXTENSION_PPTX = '.pptx'
EXTENSION_PDF = '.pdf'

# -- Post Data --
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

filename = 'nothing'

# -- Routes and Methods --
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/integration", methods=['GET', 'POST'])
def integration():
    global filename
    form = LectureUpload()
    courses = ["Signals and Communications 3","Signals and Communications 2","Engineering Mathematics 2b","Engineering Mathematics 2a", "PETARs PGEE11164"]
    if form.validate_on_submit():
        # use return topic_pdf file
        # check that the given topic_positions is of correct format
        print (form.topic_positions.data)
        # check the user input is valid
        if request.method == "POST":         
            course_1 = str(request.form['Course'])
            print('Course selected: {}'.format(course_1))
        # check the data recieved is part of the list
            if ((course_1 in courses)):
                # create list of filenames based on course selected and how many topics they want
                
                if (is_valid_topics(form.topic_positions.data)):
                    topic_list = convert_topics_to_list(form.topic_positions.data)  
                    file_name, file_extension = os.path.splitext(form.file.data.filename)
                    print('Filename: {}, Extension: {}'.format(file_name,file_extension))
                    # check if pdf format
                    if (file_extension == EXTENSION_PDF):
                        # delete integrated folder contents 
                        delete_stored_topics(INTEGRATED_PDF_DIRECTORY)
                        pdf_success = pdf(form.file.data, topic_list, course_1)
                        if (pdf_success):
                            filename = os.path.join('Integrated_PDF',UNIQUE_PDF_ID)
                            # ----- Now can pass big file to PDFSegmentor to cut into smaller chumks                            
                            segment_PDF(filename, INTEGRATED_PDF_DIRECTORY, topic_list)
                            #------
                            # generate the zip file for the whole segment_PD folder
                            generateZipFileIntegratedPDF('Integrated_PDF')
                            filename = 'Integrated_PDF.zip'
                            #----------------------
                            # delete the uploaded PDF
                            delete_stored_topics(UPLOADED_PDF_DIRECROTY)
                            return redirect(url_for('return_files'))
                        else:
                            return render_template("integration.html", title='Integration', form=form, page_number_exceeds=True,courses=courses)

                    elif (file_extension == EXTENSION_PPTX):
                        # delete integrated folder contents 
                        delete_stored_topics(INTEGRATED_PPTX_DIRECTORY)
                        pptx_success = pptx(form.file.data, topic_list, course_1)
                        if (pptx_success):
                            filename = os.path.join('Integrated_PPTX',UNIQUE_PPTX_ID)
                            # segment the powerpoints and return them with the new lecture in a zip file
                            # delete the uploaded powerpoint slide
                            delete_stored_topics(UPLOADED_PPTX_DIRECROTY)
                            return redirect(url_for('return_files'))
                        else:
                            return render_template("integration.html", title='Integration', form=form, page_number_exceeds=True,courses=courses)
                else:
                    return render_template("integration.html", title='Integration', form=form, validation=False,courses=courses)

    return render_template("integration.html", title='Integration', form=form,courses=courses)

@app.route("/download", methods=['GET', 'POST'])
def download():
    global filename
    form = LectureForm()
    courses = ["Signals and Communications 3","Signals and Communications 2","Engineering Mathematics 2b","Engineering Mathematics 2a","PETARs PGEE11164","Software Design and Modelling", "Digital Signal Analysis 4"]
    amount = [1,2,3,4,5,10,15,20,25,30,40,50,100,500]

    if request.method == "POST":            
        course_1 = str(request.form['Course'])
        amount_selected = int(str(request.form['Amount']))
        type = (request.form.get('check_PNG'),request.form.get('check_PDF'))
        #  get box tick values, 'on' = ticked, None = unticked
        png_check = type[0]
        pdf_check = type[1]

        # check the data recieved is part of the list
        if ((course_1 in courses) and (amount_selected in amount)):
            # Need to call the python script creates the Unqiue Identifiers
            print('filename after creating topic: {}.zip'.format(getTempDir()))
            PNG_dir = os.path.join('Identifier_PNG', course_1)
            PDF_dir = os.path.join('Identifier_PDF', course_1)

            # check for which files to make
            if (pdf_check == 'on' and png_check == 'on'):
                create_topic_zip_PNG_PDF(course_1,amount_selected, PNG_dir, PDF_dir)
                filename='{}.zip'.format(getTempDir())
            elif (pdf_check == 'on' and png_check == None):
                create_topic_zip_PDF(course_1,amount_selected,PDF_dir)
                filename='{}.zip'.format(getTempDir())
            elif (pdf_check == None and png_check == 'on'):
                create_topic_zip_PNG(course_1,amount_selected, PNG_dir)
                filename='{}.zip'.format(getTempDir())
            else:
                flash('Please select a file extension type!', 'danger')
                return render_template('download.html', title='Download', form=form, courses=courses, amount=amount)
            print('filename after creating topic: {}'.format(filename))

            # create the PNG file for the IDs
            #generate_id_png(course_1,amount_selected,os.path.join(IDENTIFIER_PNG_DIRECTORY,course_1))

            # return to return files so the user can download it
            return redirect(url_for('return_files'))

    return render_template('download.html', title='Download', form=form, courses=courses, amount=amount)


@app.route("/return_files")
def return_files():
    print('Filename = {}, working directory = {}'.format(filename, ROOT_DIRECTORY))
    try:
        return send_file(os.path.join(ROOT_DIRECTORY,filename), as_attachment=True )
    except Exception as e:
        return str(e)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
