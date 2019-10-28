from get_timings_class import GetTimings
import os

if __name__ == "__main__":
    cwd = os.getcwd()
    timings_class = GetTimings('small_video_tst_25s.mp4',cwd)
    timings_class.start() 