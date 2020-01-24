# logging_example.py
import logging
from config import information_dir, log_dir
import os

# Create a custom logger
logger = logging.getLogger(__name__)

# Path of log file
if (os.path.exists(log_dir)==False):
    os.mkdir(log_dir)
log_path_info  = os.path.join(log_dir,'file_info.log')
log_path_error = os.path.join(log_dir,'file_error.log')

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(log_path_error)
i_handler = logging.FileHandler(log_path_info)

c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)
i_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('[%(levelname)s]: %(message)s')
f_format = logging.Formatter('[%(levelname)s] %(message)s {File: (%(filename)s), Function: (%(funcName)s), Line: (%(lineno)d), at (%(asctime)s)}' )
i_format = logging.Formatter('[%(levelname)s] %(message)s at (%(asctime)s)')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
i_handler.setFormatter(i_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.addHandler(i_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
# logger.setLevel(logging.DEBUG)
# logger.info("Testng writing to log file")