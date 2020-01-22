
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
        self.time_array = []
        self.topic_frame_dict = {}
        self.number_of_frames = -1
        self.fps = 29.975


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

    def set_time_array(self, t_array):
        self.time_array = t_array

    def set_topic_frame_dict(self, dictionary):
        self.topic_frame_dict = dictionary

    def set_number_of_frames(self, num):
        self.number_of_frames = num

    def set_frame_rate(self, frame_rate):
        self.fps = frame_rate

# returns true if the videos are from the same lecture,
# i.e they have same code, year, date and time
def same_video(Video_1, Video_2):
    if ( (Video_1.date_time == Video_2.date_time) and (Video_1.code == Video_2.code) and (Video_1.year == Video_2.year) ):
        return True
    else:
        return False

