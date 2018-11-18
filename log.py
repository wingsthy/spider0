import logging
import logging.handlers
import os

class ColoredFormatter(logging.Formatter):
	
	def __init__(self,fmt=None,datefmt=None):
		logging.Formatter.__init__(self,fmt,datefmt)

	def format(self,record):
        COLOR_RESET =  '\033[1;0m'
        COLOR_RED = '\033[1;31m'
        COLOR_GREEN = '\033[1;32m'
        COLOR_YELLOW = '\033[1;33m'
        COLOR_BLUE = '\033[1;34,'

        LOG_COLOR = {
            'DEBUG': COLOR_BLUE + '%S' + COLOR_RESET,
            'INFO': COLOR_GREEN + '%S' + CLOOR_RESET,
            'WARNING': COLOR_YELLOW +'%S' + COLOR_RESET,
            'ERROR': COLOR_RED + '%S' + COLOR_RESET,
            'CRITICAL': COLOR_RED + '%S' + COLOR_RESET,
            }
        level_name = record.level_name
        msg = logging.Formatter.format(self,record)
        return LOG_COLOR.get(level_name, '%s') % msg

def init_log(log_path, level=logging.INFO, when="D", backup=7,
   format="[%(level_name)s]: %(asctime)s: %(filename)s:%(lineno)d %(message)s",datefmt="%m-%d %H:%M:%S"):
    formatter = logging.Formatter(format, datefmt)
    stream_formatter = ColoredFormatter(format,datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)
    
    dir = os.path.dirname(log_path)
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
        except OSError as e:
            logger.error("create log directories error : %s" % e)
            return False

    try:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
    except Exception as e:
        logger.error("stream_handler error : %s" % e)

    try:
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log", when=when,backupCount=backup)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    except IOError as e:
        logger.error("open log file error : %s" % e)
        return False

    try:
        handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log", when=when,backupCount=backup)
        handler.setLevel(logging.WARNING)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except IOError as e:
        logger.error("open log.wf file error : %s" % e)
        return False
    return True


