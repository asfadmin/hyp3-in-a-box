# hyp3_logging.py
# Rohan Weeden
# Created: June 22, 2018

# Logging setup

import logging


def getLogger(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("debug.log")
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
