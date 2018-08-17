# hyp3_logging.py
# Rohan Weeden
# Created: June 22, 2018

# Logging setup

import logging


def getLogger(name):
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler("/var/log/hyp3.log")
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
