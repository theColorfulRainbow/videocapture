import logging
import Logger

def main():
    logger = logging.getLogger("Logger")
    logger.setLevel(logging.INFO)
    # for handler in logger.handlers:
    #     handler.setLevel(logging.DEBUG)
    logger.warning("Hello")
    logger.error("test")

if __name__ == "__main__":
    main()
