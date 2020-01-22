# this class is abstract in the way it will verify if the data we recieve is vlid or not
import logging

class Verifier(object):

    def __init__(self, video):
        self.verified = False
        self.data_index = -1
        self.video = video
        self.logger = logging.getLogger("Logger")

    def verify(self, data):
        self.verified = self._verify_data(data)
        return self.verified

    # gets the iindex of the data ID e.g. if it is the 1st ID placed in the slides
    def get_data_index(self, data):
        self.data_index = self._extract_data_index(data)
        return self.data_index

    # returns the index encoded within the data
    def _extract_data_index(self,data):
        data_index = -1
        return data_index

    # verifies the data
    def _verify_data(self, data):
        verified = False
        return verified

# This class is used when you using data that encodes the course code
class CourseCodeVerifier(Verifier):

    def __init__(self, video):
        Verifier.__init__(self, video)
        self.course_code = video.code # read the course codes from a csv file and save them into here

    # check if the data is in the course codes, if not then its not verified
    def _verify_data(self, data):
        if (self.course_code in data):
            self.verified = True
            self.logger.debug("Data is Verified!")
            return True
        else:
            self.verified = False
            self.logger.debug("Data is not Verified!")
            return False

    def _extact_data_index(self, data):
        # -- Example --
        # data = "PCEh78ER i" -> where 'PCEh78ER' is the course code and 'i' is the index
        # we want the index ('i')
        # -------------
        data_index = data.split(' ', 1)[1]
        data_index = int(data_index)
        return data_index

    # in our case our key data will just be the data in raw format,
    # data = "PCEh78ER i" -> where 'PCEh78ER' is the course code and 'i' is the index
    # def _extract_key_data(data):
    #     return data

    def _extract_course_code(self, data):
        # -- Example --
        # data = "PCEh78ER i" -> where 'PCEh78ER' is the course code and 'i' is the index
        # we want the course code ('PCEh78ER')
        # -------------
        course_code = data.split(' ', 1)[0]
        return course_code

class CourseNameVerifier(Verifier):

    def __init__(self, video):
        Verifier.__init__(self, video)
        self.course_names = list()  # read the course codes from a csv file and save them into here
        self.course_names = ['Signals and Communications 2','Signals and Communications 3','Digital Signal Analysis 4','Software Design and Modelling']

    # check if the data is in the course codes, if not then its not verified
    def _verify_data(self, data):
        if (data in self.course_names):
            self.verified = True
            return True
        else:
            self.verified = False
            return False

    def _extract_data_index(self, data):
        """
        Example = "Signal and Communications 2"
        """
        dot_index = data.index('.')
        index_string = ""
        for i in range( (dot_index + 1), len(data)):
            character = data[i]
            if (character.isdigit()):
                index_string += character
            else:
                break

        return int(index_string)


    def _extract_key_data(self, data):
        return data

# this will chekc if the data given is of format
class TopicVerifier(Verifier):

    def __init__(self,video):
        Verifier.__init__(self, video)
        self.topic_names = list()  # read the course codes from a csv file and save them into here
        self.topic_name = "Topic nr."

    # check if the data is in the course codes, if not then its not verified
    def _verify_data(self, data):
        if (self.topic_name in data) and (self.video.course_name in data):
            self.verified = True
            return True
        else:
            self.verified = False
            return False

    def _extract_data_index(self, data):
        """
        Example = "Topic nr.3 Signal and Communications 2"
        """
        dot_index = data.index('.')
        index_string = ""
        for i in range( (dot_index + 1), len(data)):
            character = data[i]
            if (character.isdigit()):
                index_string += character
            else:
                break

        return int(index_string)

    # def _extract_key_data(data):
    #     return data
