import unittest
import os
import shutil
# from __init__ import Video, logger, start
import logging
import sys

unitTest_dir = (os.path.dirname(os.path.realpath(__file__)))
root_dir    = (os.path.join(unitTest_dir,".."))
video_segmenting_dir = os.path.join(root_dir,"VideoSegmenting")
sys.path.append(video_segmenting_dir)
from Segmentor import _add_topic_frame_values

class TestSegment(unittest.TestCase):

    logger = logging.getLogger("Logger")
    logger.setLevel(logging.DEBUG) 
    
    def test_empty_data(self):
        self.logger.setLevel(logging.DEBUG) 
        print("\ntest_empty_data")
        # -- Initialise Variables --
        last_topic_seen = -1
        frame_number_topic_started_at = 0
        frame_number_topic_current_at = 1
        frame_number_continous_topic_seen = 0
        frame_data_dictionary = {}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return

    def test_non_continuous(self):
        self.logger.setLevel(logging.DEBUG) 
        print("\ntest_non_continuous")
        # -- Initialise Variables --
        last_topic_seen = 2
        frame_number_topic_started_at = 101
        frame_number_topic_current_at = 104
        frame_number_continous_topic_seen = 2
        frame_data_dictionary = {1:100}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:100}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return
    
    def test_before_timeout_not_coninuous(self):
        self.logger.setLevel(logging.DEBUG) 
        print("\ntest_before_timeout_not_coninuous")
        # -- Initialise Variables --
        last_topic_seen = 1
        frame_number_topic_started_at = 120
        frame_number_topic_current_at = 121
        frame_number_continous_topic_seen = 0
        frame_data_dictionary = {1:100}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:100}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return
    
    def test_before_timeout_and_continuous(self):
        self.logger.setLevel(logging.DEBUG) 
        print("test_before_timeout_and_continuous")
        # -- Initialise Variables --
        last_topic_seen = 1
        frame_number_topic_started_at = 120
        frame_number_topic_current_at = 128
        frame_number_continous_topic_seen = 6
        frame_data_dictionary = {1:100}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:100}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return

    def test_within_time_but_not_continuous(self):
        self.logger.setLevel(logging.DEBUG) 
        print("\ntest_within_time_but_not_continuous")
        # -- Initialise Variables --
        last_topic_seen = 1
        frame_number_topic_started_at = 105
        frame_number_topic_current_at = 106
        frame_number_continous_topic_seen = 0
        frame_data_dictionary = {1:100}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:100}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return

    def test_return_to_topic_1_after_spending_8s_on_topic_2(self):
        self.logger.setLevel(logging.DEBUG) 
        print("\ntest_return_to_topic_1_after_spending_8s_on_topic_2")
        # -- Initialise Variables --
        last_topic_seen = 2
        frame_number_topic_started_at = 101
        frame_number_topic_current_at = 110
        frame_number_continous_topic_seen = 8
        frame_data_dictionary = {1:100}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:100, 2:110}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return

    def test_leave_topic_1_after_return_to_topic_1_after_spending_8s_on_topic_2(self):
        self.logger.setLevel(logging.DEBUG) 
        print("\ntest_leave_topic_1_after_return_to_topic_1_after_spending_8s_on_topic_2")
        # went from topic 1 -> topic 2. Waited 8s and returned to topic 1. Now left topic 1 after 10s
        # -- Initialise Variables --
        last_topic_seen = 1
        frame_number_topic_started_at = 109
        frame_number_topic_current_at = 125
        frame_number_continous_topic_seen = 14
        frame_data_dictionary = {1:100, 2:108}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:125}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return

    def topic_seen_after_30s_away(self):
        self.logger.setLevel(logging.DEBUG) 
        self.logger.debug("Hello")
        print("\ntopic_seen_after_30s_away")
        # went from topic 1 -> topic 2. Waited 8s and returned to topic 1. Now left topic 1 after 10s
        # -- Initialise Variables --
        last_topic_seen = 1
        frame_number_topic_started_at = 130
        frame_number_topic_current_at = 140
        frame_number_continous_topic_seen = 9
        frame_data_dictionary = {1:100, 2:115, 3:130}
        THRESHOLD_FRAME_CONTINUOUS = 5
        THRESHOLD_FRAME_TIMEOUT = 10
        # --------------------------

        # -- Expected Variables --
        expected_frame_dict = {1:100, 2:115, 3:130}
        # ------------------------  

        # -- Call Method --
        actual_dictionary = _add_topic_frame_values(frame_data_dictionary, last_topic_seen, frame_number_topic_started_at, frame_number_topic_current_at, frame_number_continous_topic_seen, THRESHOLD_FRAME_CONTINUOUS, THRESHOLD_FRAME_TIMEOUT)
        # -----------------

        self.assertDictEqual(expected_frame_dict, actual_dictionary)
        return


def main():
    #logger.setLevel(logging.DEBUG)  
    unittest.main()


if __name__ == "__main__":
    main()