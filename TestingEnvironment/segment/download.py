import requests, json, os, shutil, sys
cookieErr  = "\nCould not access Echo360. Please check your cookie data."
cook = {}

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
    for course in courses:
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and course["sectionId"] in sys.argv):
            courseTerm = terms[course["termId"]]["name"]
            downloadCourse(course,courseTerm)

def downloadCourse(course,termName):
    url = "https://echo360.org.uk/section/" + course["sectionId"] + "/syllabus"
    printlog("Downloading course: %s (%s)" % (course["courseCode"], course["courseName"]))
    resp = requests.get(url, cookies=cook)
    if os.path.isdir(termName) == False:
        os.mkdir(termName)
    if os.path.isdir(termName + "/" + course["courseCode"]) == False:
        os.mkdir(termName + "/" + course["courseCode"])
    with open(termName + "/" + course["courseCode"] + "/raw.json","wb") as jf:
        jf.write(resp.text.encode("UTF-8"))
    courseD = json.loads(resp.text)["data"]
    downloadLessonList(courseD,course["courseCode"],termName)

def downloadLessonList(lessonList,courseName,termName):
    for lesson in lessonList:
        if "groupInfo" in lesson:
            #this is not a lesson, but a group of lessons
            downloadLessonList(lesson["lessons"],courseName,termName)
        else:
            if lesson["lesson"]["hasAvailableVideo"] == True:
                #time = lesson["lesson"]["lesson"]["timing"]["start"].replace(":",".")
                try:
                    time = lesson["lesson"]["startTimeUTC"].replace(":",".")
                except:
                    time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                media = lesson["lesson"]["video"]["media"]["media"]["current"]
                #if os.path.isdir(termName + "/" + courseName + "/" + time):
                #    printlog("Error. Duplicate entry. Have you taken a course twice?")
                #    raise SystemExit
                downloadHQ(media["primaryFiles"],time,"primary.mp4",courseName,termName)
                if "secondaryFiles" in media and media["secondaryFiles"] != []:
                    downloadHQ(media["secondaryFiles"],time,"secondary.mp4",courseName,termName)
            if lesson["lesson"]["hasAvailableSlideDeck"] == True:
                try:
                    time = lesson["lesson"]["startTimeUTC"].replace(":",".")
                except:
                    time = lesson["lesson"]["lesson"]["createdAt"].replace(":",".")
                slideDeck = lesson["lesson"]["slideDeck"]["media"]["media"]["originalFile"]
                downloadResource(slideDeck["url"],time,slideDeck["name"],courseName,termName)

def downloadHQ(medias,time,type,courseName,termName):
    bestIndex = 0
    for i in range(len(medias)):
        if medias[i]["size"] > medias[bestIndex]["size"]:
            bestIndex = i
    downloadResource(medias[i]["s3Url"],time,type,courseName,termName)

def downloadResource(url,time,type,courseName,termName):
    printlog("Downloading resource: %s" % (termName + "/" + courseName + "/" + time + "/" + type))
    if os.path.isdir(termName + "/" + courseName + "/" + time) == False:
        os.mkdir(termName + "/" + courseName + "/" + time)
    if os.path.isfile(termName + "/" + courseName + "/" + time + "/" + type):
        #don't overwrite existing files
        printlog("Keeping existing file: " + time + "/" + type)
        return
    response = requests.get(url, cookies=cook, stream=True)
    if "html" in response.headers.get("content-type"):
        printlog("A html file is where a binary file (video or slides) should be.")
        printlog("This probably means the cookies in 'cookies.txt' need updating.")
        raise SystemExit
    with open(termName + "/" + courseName + "/" + time + "/" + type, 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
        del response

begin()
