'''
Unit test that segments videos in the direcotory /UnitTests/TestVideos
Main feature tested is the **start()** function from segment.py
'''

import unittest
import os
import shutil
from __init__ import Video, logger, start
import logging
from config import test_videos_scenario_perfect_dir, test_videos_scenario_secondary_empty, test_videos_scenario_topics_behind, scenario_4_2_QR_till_end

class TestSegment(unittest.TestCase):

    logger = logging.getLogger("Logger")

    # topics appear in cronological(time) order 1,2,3 in primary; 4,5,6 in secondary
    # def test_perfect_scenario(self):
    #     logger.setLevel(logging.INFO)

    #     self.logger.info("Running Test: {}".format("test_perfect_scenario"))

    #     primary_dir   = os.path.join(test_videos_scenario_perfect_dir,"video_primary.mp4")
    #     secondary_dir = os.path.join(test_videos_scenario_perfect_dir,"video_secondary.mp4")
        
    #     test_video_primary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","primary.mp4",primary_dir)
    #     test_video_secondary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4",secondary_dir)
        
    #     # make sure directory is empty
    #     self.logger.info("Emptying Desitination Directory")
    #     empty_segment_destination(test_video_primary.get_destination_directory())
    #     empty_segment_destination(test_video_secondary.get_destination_directory())        
        
    #     duo_videos = [[test_video_primary, test_video_secondary]]
    #     start(duo_videos, 5)

    #     # get number of videos in destination directory
    #     primary_videos_saved = len(next(os.walk(test_video_primary.get_destination_directory()))[2])
    #     secondary_videos_saved = len(next(os.walk(test_video_secondary.get_destination_directory()))[2])

    #     expected_number_of_primary_videos_saved = 7
    #     expected_number_of_secondary_videos_saved = 7
        
    #     self.logger.info("Primary Expected ({}) vs Actual ({})".format(expected_number_of_primary_videos_saved,primary_videos_saved))
    #     self.logger.info("Secondary Expected ({}) vs Actual ({})".format(expected_number_of_secondary_videos_saved, secondary_videos_saved))
        
    #     self.assertEquals(expected_number_of_primary_videos_saved, primary_videos_saved)
    #     self.assertEquals(expected_number_of_secondary_videos_saved, secondary_videos_saved)

    #     return None
    

    # # # secondary video has no QR codes
    # def test_scenario_secondary_empty(self):
    #     logger.setLevel(logging.INFO)

    #     self.logger.info("Running Test: {}".format("test_scenario_secondary_empty"))

    #     primary_dir   = os.path.join(test_videos_scenario_secondary_empty,"video_primary.mp4")
    #     secondary_dir = os.path.join(test_videos_scenario_secondary_empty,"video_secondary.mp4")
        
    #     test_video_primary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","primary.mp4",primary_dir)
    #     test_video_secondary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4",secondary_dir)

    #     # make sure directory is empty
    #     self.logger.info("Emptying Desitination Directory")
    #     empty_segment_destination(test_video_primary.get_destination_directory())
    #     empty_segment_destination(test_video_secondary.get_destination_directory())        
        
    #     duo_videos = [[test_video_primary, test_video_secondary]]
    #     start(duo_videos, 5)

    #     # get number of videos in destination directory
    #     primary_videos_saved = len(next(os.walk(test_video_primary.get_destination_directory()))[2])
    #     secondary_videos_saved = len(next(os.walk(test_video_secondary.get_destination_directory()))[2])
        
    #     expected_number_of_primary_videos_saved = 4
    #     expected_number_of_secondary_videos_saved = 4
        
    #     self.logger.info("Primary Expected ({}) vs Actual ({})".format(expected_number_of_primary_videos_saved,primary_videos_saved))
    #     self.logger.info("Secondary Expected ({}) vs Actual ({})".format(expected_number_of_secondary_videos_saved, secondary_videos_saved))
        
    #     self.assertEquals(expected_number_of_primary_videos_saved, primary_videos_saved)
    #     self.assertEquals(expected_number_of_secondary_videos_saved, secondary_videos_saved)

    #     return None

    # # # # topics 4, 5, 6 appear before 1,2,3
    # def test_topics_not_ordered(self):
    #     logger.setLevel(logging.INFO)  

    #     self.logger.info("Running Test: {}".format("topics_not_ordered"))

    #     primary_dir   = os.path.join(test_videos_scenario_topics_behind,"video_primary.mp4")
    #     secondary_dir = os.path.join(test_videos_scenario_topics_behind,"video_secondary.mp4")
        
    #     test_video_primary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","primary.mp4",primary_dir)
    #     test_video_secondary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4",secondary_dir)
        
    #     # make sure directory is empty
    #     self.logger
    #     empty_segment_destination(test_video_primary.get_destination_directory())
    #     empty_segment_destination(test_video_secondary.get_destination_directory())

    #     # make sure directory is empty
    #     empty_segment_destination(test_video_primary.get_destination_directory())
    #     empty_segment_destination(test_video_secondary.get_destination_directory())        
        
    #     duo_videos = [[test_video_primary, test_video_secondary]]
    #     start(duo_videos, 1)

    #     # get number of videos in destination directory
    #     primary_videos_saved = (next(os.walk(test_video_primary.get_destination_directory()))[2])
    #     secondary_videos_saved = (next(os.walk(test_video_secondary.get_destination_directory()))[2])

    #     expected_primary_names = ["SCEE08007_2020_01_17T12:00Z_primary_topic_1.mp4", "SCEE08007_2020_01_17T12:00Z_primary_topic_2.mp4","SCEE08007_2020_01_17T12:00Z_primary_topic_3.mp4","SCEE08007_2020_01_17T12:00Z_primary_topic_4.mp4"]
    #     expected_secondary_names = ["SCEE08007_2020_01_17T12:00Z_secondary_topic_1.mp4", "SCEE08007_2020_01_17T12:00Z_secondary_topic_2.mp4","SCEE08007_2020_01_17T12:00Z_secondary_topic_3.mp4", "SCEE08007_2020_01_17T12:00Z_secondary_topic_4.mp4"]
        
    #     self.logger.info("Primary Expected ({}) vs Actual ({})".format(expected_primary_names,primary_videos_saved))
    #     self.logger.info("Secondary Expected ({}) vs Actual ({})".format(expected_secondary_names, secondary_videos_saved))

    #     self.assertCountEqual(expected_primary_names, primary_videos_saved)
    #     self.assertCountEqual(expected_secondary_names, secondary_videos_saved)
    #     return None

    def test_4_2_QR_till_end(self):       
        logger.setLevel(logging.INFO)  

        self.logger.info("Running Test: {}".format("topics_not_ordered"))

        primary_dir   = os.path.join(scenario_4_2_QR_till_end,"video_primary.mp4")
        secondary_dir = os.path.join(scenario_4_2_QR_till_end,"video_secondary.mp4")
        
        test_video_primary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","primary.mp4",primary_dir)
        test_video_secondary = Video("SCEE08007","2019-2020","2020-01-17T12:00Z","secondary.mp4",secondary_dir)
    
        # make sure directory is empty
        self.logger
        empty_segment_destination(test_video_primary.get_destination_directory())
        empty_segment_destination(test_video_secondary.get_destination_directory())

        # make sure directory is empty
        empty_segment_destination(test_video_primary.get_destination_directory())
        empty_segment_destination(test_video_secondary.get_destination_directory())        
        
        duo_videos = [[test_video_primary, test_video_secondary]]
        start(duo_videos, 1)

        # get number of videos in destination directory
        primary_videos_saved = (next(os.walk(test_video_primary.get_destination_directory()))[2])
        secondary_videos_saved = (next(os.walk(test_video_secondary.get_destination_directory()))[2])

        expected_primary_names = ["SCEE08007_2020_01_17T12:00Z_primary_topic_1.mp4", "SCEE08007_2020_01_17T12:00Z_primary_topic_2.mp4","SCEE08007_2020_01_17T12:00Z_primary_topic_3.mp4","SCEE08007_2020_01_17T12:00Z_primary_topic_4.mp4", "SCEE08007_2020_01_17T12:00Z_primary_topic_5.mp4", "SCEE08007_2020_01_17T12:00Z_primary_topic_6.mp4"]
        expected_secondary_names = ["SCEE08007_2020_01_17T12:00Z_secondary_topic_1.mp4", "SCEE08007_2020_01_17T12:00Z_secondary_topic_2.mp4","SCEE08007_2020_01_17T12:00Z_secondary_topic_3.mp4", "SCEE08007_2020_01_17T12:00Z_secondary_topic_4.mp4", "SCEE08007_2020_01_17T12:00Z_secondary_topic_5.mp4", "SCEE08007_2020_01_17T12:00Z_secondary_topic_6.mp4"]
        
        self.logger.info("Primary Expected ({})\nvs Actual\n({})\n".format(expected_primary_names,primary_videos_saved))
        self.logger.info("Secondary Expected ({})\nvs Actual\n({})\n".format(expected_secondary_names, secondary_videos_saved))

        self.assertCountEqual(expected_primary_names, primary_videos_saved)
        self.assertCountEqual(expected_secondary_names, secondary_videos_saved)
        return None

# delete folders where segmented video will appear for given video
def empty_segment_destination(video_dir):
    if(os.path.isdir(video_dir)):
        shutil.rmtree(video_dir)
    return None

def main():
    unittest.main()


if __name__ == "__main__":
    main()
