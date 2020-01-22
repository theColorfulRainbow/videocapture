import requests, json, os, shutil, sys
import pandas as pd
from Video import Video
import logging
import Logger
from Subject import *

cookieErr  = "\nCould not access Echo360. Please check your cookie data."
cook = {}
dowloaded_videos_path = os.path.join(os.getcwd(),"Videos/downloaded_videos")   # ensures the vidoes are downaloded in the "downloaded_videos" folder
to_segment_videos = []  # (path_to_video,course_code)
COURSE_CSV_FILE = os.path.join(os.getcwd(), "Docs/subject.csv")
logger = logging.getLogger("Logger")

def _save_to_csv(course_code, year_active, date_time, video_type, csv):
    csv_entry = ("{},{},{}\n".format(year_active,date_time,video_type))
    with open(csv,'a') as fd:
        fd.write(csv_entry)

def _get_participating_courses():
    participating_courses = Subject_List(COURSE_CSV_FILE).subject_set  # will contain corse code of all participating subjects
    logger.info("Courses Participating: {}".format(participating_courses))
    return participating_courses

def _remove_courses_not_involved_in_project(courses):
    participating_courses = _get_participating_courses()
    courses_out = []
    for i in range(len(courses)):
        course = courses[i]
        logger.debug(course)
        #logger.debug("Year Active: {}".format(course["yearActive"]))
        # if course["courseCode"] not in participating_courses.code:
        for subject in participating_courses:
            # check if code is correct and year actieve as well (2019-0 means 2019-2020)
            if (subject.code == course["courseCode"] and ('2019-0' in str(course['sectionName']))):
                courses_out.append(course)
                break

    return courses_out

def _already_downloaded(date_time,video_type,courseCode,year_active):
    csv_file_name = "{}.csv".format(courseCode)
    csv_file = pd.read_csv(open(os.path.join("Records",csv_file_name),'r'), encoding='utf-8', engine='c')
    in_csv = False

    logger.debug("Already Dowloaded:: date_time: {}, video_type: {}, courseCode: {}, year active: {}".format(date_time,video_type,courseCode,year_active))
    # read the csv file and check if we have already downloaded this video
    for line in csv_file.values:
        year_started=line[0]
        date_time_uploaded=line[1]
        video_number=line[2]

        logger.debug("Year Started: {}, Date_time_uploaded: {}, video_number: {}\n\n".format(year_started, date_time_uploaded, video_number))
        # check if we have a match
        if (year_started == year_active and date_time_uploaded == date_time and video_number == video_type):
            in_csv = True

    return in_csv


def _printlog(msg):
    with open("log.txt","a") as lF:
        lF.write("\n" + msg)
    logger.debug(msg)

def _getCookies():
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


def _getEnrollments():
    resp = requests.get("https://echo360.org.uk/user/enrollments",cookies=cook)
    try:
        with open("enrollment.json","wb") as jf:
            jf.write(resp.text.encode("UTF-8"))
        jd = json.loads(resp.text)
        courses = jd["data"][0]["userSections"]
        terms = jd["data"][0]["termsById"]
        return (courses,terms)
    except:
        _printlog("Error. Could not access signed-in Echo360.")
        _printlog("Make sure you have up-to-date cookies in 'cookies.txt'")
        raise SystemExit

def begin():
    global cook
    cook = _getCookies()
    (courses,terms) = _getEnrollments()

    # remove courses that are not involved in the project
    courses = _remove_courses_not_involved_in_project(courses)

    for course in courses:
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and course["sectionId"] in sys.argv):
            courseTerm = terms[course["termId"]]["name"]
            downloadCourse(course,courseTerm)

    return to_segment_videos

def downloadCourse(course,year_active):
    url = "https://echo360.org.uk/section/" + course["sectionId"] + "/syllabus"
    _printlog("Downloading course: %s (%s)" % (course["courseCode"], course["courseCode"]))
    resp = requests.get(url, cookies=cook)
    if os.path.isdir(dowloaded_videos_path) == False:
        os.mkdir(dowloaded_videos_path)
    if os.path.isdir(os.path.join(dowloaded_videos_path, year_active)) == False:
        os.mkdir(os.path.join(dowloaded_videos_path, year_active))
    if os.path.isdir( os.path.join(dowloaded_videos_path, year_active, course["courseCode"]) ) == False:
        os.mkdir(os.path.join(dowloaded_videos_path, year_active, course["courseCode"]))
    with open(os.path.join(dowloaded_videos_path, year_active, course["courseCode"],"raw.json"),"wb") as jf:
        jf.write(resp.text.encode("UTF-8"))
    courseD = json.loads(resp.text)["data"]
    downloadLessonList(courseD,course["courseCode"],year_active)

def downloadLessonList(lessonList,courseCode,year_active):
    for lesson in lessonList:
        if "groupInfo" in lesson:
            #this is not a lesson, but a group of lessons
            downloadLessonList(lesson["lessons"],courseCode,year_active)
        else:
            if lesson["lesson"]["hasAvailableVideo"] == True:
                #date_time = lesson["lesson"]["lesson"]["timing"]["start"].replace(":",".")
                try:
                    date_time = lesson["lesson"]["startTimeUTC"].replace(":",".")
                except:
                    date_time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                media = lesson["lesson"]["video"]["media"]["media"]["current"]
                #if os.path.isdir(year_active + "/" + courseCode + "/" + date_time):
                #    _printlog("Error. Duplicate entry. Have you taken a course twice?")
                #    raise SystemExit
                _downloadHQ(media["primaryFiles"],date_time,"primary.mp4",courseCode,year_active)
                if "secondaryFiles" in media and media["secondaryFiles"] != []:
                    _downloadHQ(media["secondaryFiles"],date_time,"secondary.mp4",courseCode,year_active)
            if lesson["lesson"]["hasAvailableSlideDeck"] == True:
                try:
                    date_time = lesson["lesson"]["startTimeUTC"].replace(":",".")
                except:
                    date_time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                slideDeck = lesson["lesson"]["slideDeck"]["media"]["media"]["originalFile"]
                _downloadResource(slideDeck["url"],date_time,slideDeck["name"],courseCode,year_active)



def _downloadHQ(medias,date_time,video_type,courseCode,year_active):
    bestIndex = 0
    for i in range(len(medias)):
        if medias[i]["size"] > medias[bestIndex]["size"]:
            bestIndex = i
    _downloadResource(medias[i]["s3Url"],date_time,video_type,courseCode,year_active)

def _downloadResource(url,date_time,video_type,courseCode,year_active):
    _printlog("Downloading resource: %s" % (year_active + "/" + courseCode + "/" + date_time + "/" + video_type))
    video_path = dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time + "/" + video_type

    csv_file_name = "{}.csv".format(courseCode)
    csv_file_name = os.path.join("Records",csv_file_name)

    if (_already_downloaded(date_time, video_type, courseCode, year_active)):
        logger.debug("Course: {} - {} - {} has already been downloaded".format(courseCode, date_time, year_active))
        return

    if os.path.isdir(dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time) == False:
        os.mkdir(dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time)

    response = requests.get(url, cookies=cook, stream=True)
    if "html" in response.headers.get("content-type"):
        _printlog("A html file is where a binary file (video or slides) should be.")
        _printlog("This probably means the cookies in 'cookies.txt' need updating.")
        raise SystemExit
    # downloads the lecture from echo360
    with open(dowloaded_videos_path + "/" + year_active + "/" + courseCode + "/" + date_time + "/" + video_type, 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
        del response

    # save downloaded data to csv
    _save_to_csv(courseCode, year_active,date_time, video_type, csv_file_name)
    this_video = Video(courseCode, year_active, date_time, video_type, video_path)
    # save video path to to_segment_videos
    to_segment_videos.append(this_video)
    logger.info("Successfully Downloaded: {}".format(this_video))

begin()
