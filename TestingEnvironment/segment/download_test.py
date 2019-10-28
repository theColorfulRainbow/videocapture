import requests, json, os, shutil, sys
import pandas as pd
from Video import Video
import logging
import Logger

cookieErr  = "\nCould not access Echo360. Please check your cookie data."
cook = {}
dowloaded_videos_path = os.path.join(os.getcwd(),"downloaded_videos")   # ensures the vidoes are downaloded in the "downloaded_videos" folder
to_segment_videos = []  # (path_to_video,course_code)
COURSES = []
logger = logging.getLogger("Logger")

def save_to_csv(course_code, year_active, date_time, video_type, csv):
    csv_entry = ("{},{},{}\n".format(year_active,date_time,video_type))
    with open(csv,'a') as fd:
        fd.write(csv_entry)

def remove_courses_not_involved_in_project(courses):
    participating_courses = ["SCEE08007"]  # will contain corse code of all participating subjects
    courses_out = []
    for i in range(len(courses)):
        course = courses[i]
        if course["courseCode"] not in participating_courses:
            pass
        else:
            courses_out.append(course)
    return courses_out


def already_downloaded(date_time,video_type,courseCode,year_active):
    csv_file_name = "{}.csv".format(courseCode)
    csv_file = pd.read_csv(open(os.path.join("Records",csv_file_name),'r'), encoding='utf-8', engine='c')
    in_csv = False

    # logger.debug("Already Dowloaded:: date_time: {}, video_type: {}, courseCode: {}, year active: {}".format(date_time,video_type,courseCode,year_active))
    # read the csv file and check if we have already downloaded this video
    for line in csv_file.values:
        year_started=line[0]
        date_time_uploaded=line[1]
        video_number=line[2]

        # logger.debug("Year Started: {}, Date_time_uploaded: {}, video_number: {}\n\n".format(year_started, date_time_uploaded, video_number))
        # check if we have a match
        if (year_started == year_active and date_time_uploaded == date_time and video_number == video_type):
            in_csv = True

    return in_csv




def printlog(msg):
    with open("log.txt","a") as lF:
        lF.write("\n" + msg)
    logger.debug(msg)

def getCookies():
    cookies = {}
    with open("cookies.txt","r") as cFile:
        cookie = {}
        for ck in cFile:
            if ck.strip()[0] == "#": continue
            cookieDomain = ck.strip().split("\t")[0]
            if "echo360.org.uk" not in cookieDomain: continue
            try:
                cookieName = ck.strip().split("\t")[5]
                cookieData = ck.strip().split("\t")[6]
                if cookieName == "PLAY_SESSION": cookieData = cookieData.replace("&amp;","&")
                cookies[cookieName] = cookieData
            except:
                pass #stupid incorrectly-formatted data
    return cookies

def getEnrollments():
    resp = requests.get("https://echo360.org.uk/user/enrollments",cookies=cook)
    try:
        with open("enrollment.json","wb") as jf:
            jf.write(resp.text.encode("UTF-8"))
        jd = json.loads(resp.text)
        courses = jd["data"][0]["userSections"]
        # logger.debug("Courses: {}".format(courses))
        terms = jd["data"][0]["termsById"]
        return (courses,terms)
    except:
        printlog("Error. Could not access signed-in Echo360.")
        printlog("Make sure you have up-to-date cookies in 'cookies.txt'")
        raise SystemExit

def begin():
    global cook
    cook = getCookies()
    (courses,terms) = getEnrollments()
    logger.debug(courses)
    # exit()

    # remove courses that are not involved in the project
    courses = remove_courses_not_involved_in_project(courses)
    for course in courses:
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and course["sectionId"] in sys.argv):
            courseTerm = terms[course["termId"]]["name"]
            # downloadCourse(course,courseTerm)
            logger.debug('\ncourse = {}\ncourseTerm = {}'.format(course,courseTerm))
            exit()

def downloadCourse(course,year_active, date):
    url = "https://echo360.org.uk/section/" + course["sectionId"] + "/syllabus"
    printlog("Downloading course: %s (%s)" % (course["courseCode"], course["courseCode"]))
    resp = requests.get(url, cookies=cook)
    if os.path.isdir(dowloaded_videos_path) == False:
        os.mkdir(dowloaded_videos_path)
    if os.path.isdir(year_active) == False:
        os.mkdir(year_active)
    if os.path.isdir(dowloaded_videos_path + "/" + year_active + "/" + course["courseCode"]) == False:
        os.mkdir(dowloaded_videos_path + "/" + year_active + "/" + course["courseCode"])
    with open(dowloaded_videos_path + "/" + year_active + "/" + course["courseCode"] + "/raw.json","wb") as jf:
        jf.write(resp.text.encode("UTF-8"))
    courseD = json.loads(resp.text)["data"]
    downloadLessonList(courseD,course["courseCode"],year_active, date)

def downloadLessonList(lessonList,courseCode,year_active,date):
    for lesson in lessonList:

        if "groupInfo" in lesson:
            #this is not a lesson, but a group of lessons
            downloadLessonList(lesson["lessons"],courseCode,year_active)
        else:
            # check that it's the date you are interested in before downloading
            if((date in lesson["lesson"]["lesson"]["timing"]["start"]) == True or date==None):
                if lesson["lesson"]["hasAvailableVideo"] == True:
                    #date_time = lesson["lesson"]["lesson"]["timing"]["start"].replace(":",".")
                    try:
                        date_time = lesson["lesson"]["startdate_timeUTC"].replace(":",".")
                    except:
                        date_time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                    media = lesson["lesson"]["video"]["media"]["media"]["current"]
                    #if os.path.isdir(year_active + "/" + courseCode + "/" + date_time):
                    #    printlog("Error. Duplicate entry. Have you taken a course twice?")
                    #    raise SystemExit
                    downloadHQ(media["primaryFiles"],date_time,"primary.mp4",courseCode,year_active)
                    if "secondaryFiles" in media and media["secondaryFiles"] != []:
                        downloadHQ(media["secondaryFiles"],date_time,"secondary.mp4",courseCode,year_active)
                if lesson["lesson"]["hasAvailableSlideDeck"] == True:
                    try:
                        date_time = lesson["lesson"]["startdate_timeUTC"].replace(":",".")
                    except:
                        date_time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                    slideDeck = lesson["lesson"]["slideDeck"]["media"]["media"]["originalFile"]
                    downloadResource(slideDeck["url"],date_time,slideDeck["name"],courseCode,year_active)

def downloadHQ(medias,date_time,video_type,courseCode,year_active):
    bestIndex = 0
    for i in range(len(medias)):
        if medias[i]["size"] > medias[bestIndex]["size"]:
            bestIndex = i
    downloadResource(medias[i]["s3Url"],date_time,video_type,courseCode,year_active)


def downloadResource(url,date_time,video_type,courseCode,year_active):
    printlog("Downloading resource: %s" % (year_active + "/" + courseCode + "/" + date_time + "/" + video_type))
    video_path = dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time + "/" + video_type

    csv_file_name = "{}.csv".format(courseCode)
    csv_file_name = os.path.join("Records",csv_file_name)

    if (already_downloaded(date_time, video_type, courseCode, year_active)):
        logger.debug("Course: {} - {} - {} has already been downloaded".format(courseCode, date_time, year_active))
        return

    if os.path.isdir(dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time) == False:
        os.mkdir(dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time)

    response = requests.get(url, cookies=cook, stream=True)
    if "html" in response.headers.get("content-type"):
        printlog("A html file is where a binary file (video or slides) should be.")
        printlog("This probably means the cookies in 'cookies.txt' need updating.")
        raise SystemExit
    # downloads the lecture from echo360
    with open(dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time + "/" + video_type, 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
        del response

    # save downloaded data to csv
    save_to_csv(courseCode, year_active,date_time, video_type, csv_file_name)
    this_video = Video(courseCode, year_active, date_time, video_type, video_path)
    COURSES.append(this_video)
    logger.info("Successfully Downloaded: {}".format(this_video))
    # # save video path to to_segment_videos
    # to_segment_videos.append([video_path,courseCode])

# download specific lectures given course name and date lecture was taken
def download_lecture(name,date,course_term):
    global cook
    cook = getCookies()
    (courses,terms) = getEnrollments()
    for course in courses:
        if (course['courseName']==name):
            if len(sys.argv) == 1 or (len(sys.argv) > 1 and course["sectionId"] in sys.argv):
                courseTerm = terms[course["termId"]]["name"]
                if(courseTerm == course_term):
                    downloadCourse(course,courseTerm,date)
                    logger.debug('\ncourse = {}\ncourseTerm = {}'.format(course,courseTerm))
                    # exit()
                else:
                    logger.debug('not in course term')
                    logger.debug(courseTerm)
        else:
            logger.debug('Not in course names')
            logger.debug(course['courseCode'])

    logger.debug("Finished Downloading returning: {}".format(COURSES))
    return COURSES

# download_lecture('Signals and Communication Systems 2','2019-08-02','2017-2018')

# if __name__ == '__main__':
    # downloadCourse("SCEE080072017-8SV1SEM2")
