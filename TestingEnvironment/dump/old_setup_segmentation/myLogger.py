import logging
	
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)

f_handler = logging.FileHandler('LogFile.log')
f_handler.setLevel(logging.ERROR)

c_format = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)5s()] [%(name)s %(levelname)s] : %(message)s')
c_handler.setFormatter(c_format)

f_format = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)5s()] %(asctime)s -- [%(name)s %(levelname)s] : %(message)s')
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)

if __name__ == '__main__':
	print(__name__)
