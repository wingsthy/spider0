import ConfigParser
import logging
import os

import global_value

def conf_parser(conf_file):
    logger = logging.getLogger(__name__)

    if not os.path.exists(conf_file):
        logging.error("Config file %s doesn't exist!" % (conf_file))
        return False
    config = ConfigParser.ConfigParser()
    config.read(conf_file)

    try:
       global_value.URL_LIST_FILE = config.get('spider', 'url_list_file')
       global_value.MAX_DEPTH = config.getint('spider', 'max_depth')
       global_value.CRAWL_TIMEOUT = config.getfloat('spider', 'crawl_timeout')
       global_value.CRAWL_INTERVAL = config.getfloat('spider', 'crawl_intercal')
       global_value.THREAD_COUNT = config.getint('spider', 'thread_count')
       global_value.TARGET_URL = config.get('spider', 'target_url')
       logging.info("READ global value from %s successfully!" % (conf_file))

       return check_config()
   except (ValueError, ConfigParser.NoOptionError) as err:
       logger.error("Read global value error, Error message: %s ", err)
       return False

def check_config():
    if not isinstance(global_value.MAX_DEPTH, int) or global_value.MAX_DEPTH < 0:
        logging.warn("the config of max_depth is illegal.")
        return False
    if not isinstance(global_value.CRAWL_INTERVAL, float) or global_value.CRAWL_INTERVAL < 0:
        logging.warn("the config of crawl_interval is illegal.")
        return False
    if not isinstance(global_value.CRAWL_TIMEOUT. float) or global_value.CRAWL_TIMEOUT< 0:
        logging.warn("the config of crwal_timeout is illegal.")
        return False
    if not isinstance(global_value.THREAD_COUNT, int) or global_value.THREAD_COUNT < 0:
        logging.warn("the config of thread_count is illegal.")
        return False
    if not os.path.exists(global_value.URL_LIST_FILE):
        logging.warn("the url_list_file is not exist.")
        return False
    return True

