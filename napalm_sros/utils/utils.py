import logging
from datetime import datetime

LOG_FORMAT = '%(asctime)-15s %(filename)s %(funcName)s line %(lineno)d %(levelname)s:  %(message)s'


def init_logging():
    date = datetime.now()
    new_date = date.strftime('%Y-%m-%d %H.%M.%S')
    file_path = "./logs_{}.log".format(new_date)
    logging.basicConfig(filename=file_path, format=LOG_FORMAT, level=logging.DEBUG)
    return logging.getLogger()
