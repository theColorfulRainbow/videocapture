
" used to contain information about a course we have downloaded and are to segment"
class Video(object):

    def __init__(self,code,year_active,date_time,video_type, video_path):
        self.initialize_variables(code,year_active,date_time,video_type, video_path)

    def initialize_variables(self,code,year_active,date_time,video_type, video_path):
        self.date_time  = date_time
        self.code       = code
        self.year       = year_active
        self.video_type = video_type
        self.path       = video_path

    def __repr__(self):
        represntation = "{} with date and time: {} {}".format(self.code, self.date_time, self.video_type.split(".")[0])
        return represntation

    def get_video_name(self):
        datetime = self.date_time.replace("-","_")
        datetime = datetime.replace(".","_")
        video_name = "{}_{}_{}".format(self.code,datetime,self.video_type.split(".")[0])
        return video_name

    def get_video_path(self):
        return self.path
