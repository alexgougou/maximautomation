"""
@Author  : alex
@Time    : 2019/1/10 10:30
@describe: 日志类
"""
import os
import os.path
import socket
import logging
import logging.handlers
logging.basicConfig()


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class LogInfo(object):
    logs = logging.getLogger()

    def __init__(self):
        host_name = socket.gethostname()
        logging_msg_format = '[%(asctime)s] [%(levelname)s] [' + host_name + '][%(module)s.py - line:%(lineno)d] %(message)s'
        logging_data_format = '%Y-%m-%d %H:%M:%S'
        log_dirpath = 'logs'
        logging.basicConfig(level=logging.INFO, format=logging_msg_format,datefmt=logging_data_format)
        self.logs.setLevel(logging.INFO)

        if not os.path.exists(log_dirpath):
            os.mkdir(log_dirpath)
        log_file = os.path.join(log_dirpath, 'system.log')

        file_handler = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1)
        file_handler.setFormatter(logging.Formatter(logging_msg_format))
        self.logs.addHandler(file_handler)

    def get_logs(self):
        return self.logs
