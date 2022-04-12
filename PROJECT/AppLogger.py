import logging
from datetime import datetime

class AppLogger:

    logging.basicConfig(filename='applog.log', level=logging.INFO)

    def __init__(self, classname):
        self.className = classname

    def log(self, msg):
        logging.info(str(datetime.today()) + ' ' + self.className + ' : ' + msg)

    def log(self, msg):
        logging.error(str(datetime.today()) + ' ' + self.className + ' : ' + msg)
