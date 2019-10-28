# logging_example.py
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('[%(levelname)s]: %(message)s')
f_format = logging.Formatter('Level: [%(levelname)s] %(message)s {File: (%(filename)s), Function: (%(funcName)s), Line: (%(lineno)d), at (%(asctime)s)}' )
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
