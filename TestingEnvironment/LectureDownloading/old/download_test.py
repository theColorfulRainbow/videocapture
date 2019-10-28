import requests, json, os, shutil, sys
cookieErr  = "\nCould not access Echo360. Please check your cookie data."
cook = {}

def save_to_csv(course_code, year_active, date_time, video_type, csv):
    csv_entry = ("{},{},{}".format(year_active,date_time,video_type))
    with open(csv,'a') as fd:
        fd.write(csv_entry)

def remove_courses_not_involved_in_project(courses):
    participating_courses = ["SCEE08007"]  # will contain corse code of all participating subjects

    for course in courses:
        if course["courseCode"] not in participating_courses:
            del courses[course]
    return courses


def already_downloaded(date_time,video_type,courseCode,year_active):
    csv_file_name = "{}.csv".format(courseCode)
    csv_file = pd.read_csv(open(os.path.join("Records",csv_file_name),'r'), encoding='utf-8', engine='c')
    in_csv = False

    print("Already Dowloaded:: date_time: {}, video_type: {}, courseCode: {}, year active: {}".format(date_time,video_type,courseCode,year_active))
    # read the csv file and check if we have already downloaded this video
    for line in csv_file.values:
        year_started=line[0]
        date_time_uploaded=line[1]
        video_number=line[2]

        print("Year Started: {}, Date_time_uploaded: {}, video_number: {}\n\n".format(year_started, date_time_uploaded, video_number))
        # check if we have a match
        if (year_started == year_active and date_time_uploaded == date_time and video_number == video_type):
            in_csv = True

    return in_csv


def printlog(msg):
    with open("log.txt","a") as lF:
        lF.write("\n" + msg)
    print(msg)

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
    print("Hello {}".format(courses))
    # remove courses that are not involved in the project
    courses = remove_courses_not_involved_in_project(courses)

    for course in courses:
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and course["sectionId"] in sys.argv):
            courseTerm = terms[course["termId"]]["name"]
            downloadCourse(course,courseTerm)

def downloadCourse(course,date_active):
    url = "https://echo360.org.uk/section/" + course["sectionId"] + "/syllabus"
    printlog("Downloading course: %s (%s)" % (course["courseCode"], course["courseName"]))
    resp = requests.get(url, cookies=cook)
    if os.path.isdir(date_active) == False:
        os.mkdir(date_active)
    if os.path.isdir(date_active + "/" + course["courseCode"]) == False:
        os.mkdir(date_active + "/" + course["courseCode"])
    with open(date_active + "/" + course["courseCode"] + "/raw.json","wb") as jf:
        jf.write(resp.text.encode("UTF-8"))
    courseD = json.loads(resp.text)["data"]
    downloadLessonList(courseD,course["courseCode"],date_active)

def downloadLessonList(lessonList,courseName,date_active):
    for lesson in lessonList:
        if "groupInfo" in lesson:
            #this is not a lesson, but a group of lessons
            downloadLessonList(lesson["lessons"],courseName,date_active)
        else:
            if lesson["lesson"]["hasAvailableVideo"] == True:
                #date_time = lesson["lesson"]["lesson"]["timing"]["start"].replace(":",".")
                try:
                    date_time = lesson["lesson"]["startTimeUTC"].replace(":",".")
                except:
                    date_time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                media = lesson["lesson"]["video"]["media"]["media"]["current"]
                #if os.path.isdir(date_active + "/" + courseName + "/" + date_time):
                #    printlog("Error. Duplicate entry. Have you taken a course twice?")
                #    raise SystemExit
                downloadHQ(media["primaryFiles"],date_time,"primary.mp4",courseName,date_active)
                if "secondaryFiles" in media and media["secondaryFiles"] != []:
                    downloadHQ(media["secondaryFiles"],date_time,"secondary.mp4",courseName,date_active)
            if lesson["lesson"]["hasAvailableSlideDeck"] == True:
                try:
                    date_time = lesson["lesson"]["startTimeUTC"].replace(":",".")
                except:
                    date_time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                slideDeck = lesson["lesson"]["slideDeck"]["media"]["media"]["originalFile"]
                downloadResource(slideDeck["url"],date_time,slideDeck["name"],courseName,date_active)



def downloadHQ(medias,date_time,video_type,courseName,date_active):
    bestIndex = 0
    for i in range(len(medias)):
        if medias[i]["size"] > medias[bestIndex]["size"]:
            bestIndex = i
    downloadResource(medias[i]["s3Url"],date_time,video_type,courseName,date_active)

def downloadResource(url,date_time,video_type,courseName,date_active):
    printlog("Downloading resource: %s" % (date_active + "/" + courseName + "/" + date_time + "/" + video_type))

    # if os.path.isfile(date_active + "/" + courseName + "/" + date_time + "/" + video_type):
    #     #don't overwrite existing files
    #     printlog("Keeping existing file: " + date_time + "/" + video_type)
    #     return
    if (already_downloaded(date_time, video_type, courseCode, year_active)):
        print("Course: {} - {} - {} has already been downloaded".format(courseCode, date_time, year_active))
        return

    if os.path.isdir(date_active + "/" + courseName + "/" + date_time) == False:
        os.mkdir(date_active + "/" + courseName + "/" + date_time)

    response = requests.get(url, cookies=cook, stream=True)
    if "html" in response.headers.get("content-video_type"):
        printlog("A html file is where a binary file (video or slides) should be.")
        printlog("This probably means the cookies in 'cookies.txt' need updating.")
        raise SystemExit
    with open(date_active + "/" + courseName + "/" + date_time + "/" + video_type, 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
        del response

    # save downloaded data to csv
    save_to_csv(courseCode, year_active,date_time, video_type, csv_file_name)

begin()
