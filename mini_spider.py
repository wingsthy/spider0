import argparse
import log
import logging
import Queue
import sys
import threading
import time

import config_load
import global_value
import url_item
import webpage_utils

class SpiderThread(threading.Thread):
    def __init__(self,url_queue,lock,crawed_urls):
    super(SpiderThread,self).__init__()
    self.url_queue = url_queue
    self.lock = lock
    self/crawed_urls = crawed_urls
    self.is_sleep = 0

    def run(self)
        while True:
            if not self.url_queue.empty():
                try:
                    url = self.url_queue.getnowait()    
                    self.is_sleep = 0
                except Queue.Empty:
                    if self.is_sleep > global_value.MAXDEPTH:
                        logging.info("url queue now is empty and thread sleep to long time, \ thread quit")
                    else self.is_sleep += 1:
                        logging.info("url queue now is empty, thread start sleep!")
                        time.sleep(global_value.CRAWL_TIMEOUT + global_value.CRAWL_INTERVAL)
                        continue
                    else:
                        if self.is_sleep > global_value.MAX_DEPTH:
                            logging.info("url queue now is empty and thread sleep to long time, \ thread quit!")
                            break
                        else:
                            self.is_sleep += 1
                            logging.info("url queue now is empty,, thread start sleep!")
                            time.sleep(global_value.CRAWL_TIMEOUT + global_value.CRAWL_INTERVAL)
                            continue
                    if url.depth >= global_value.MAX_DEPTH:
                        logging.info("url %s has reach max depth %s",url.url, global_value.MAX_DEPTH)
                        self.url_queue.task_done()
                        continue
                    elif url.url in self.crawed_urls:
                        logging.info("url %s has crawed", url.url)
                        self.url_queue.task_done()
                        continue

                    with self.lock:
                        self.crawed_urls.add(url.url)
                        if content:
                            urls = web_tools.parse_url(content, url.url)
                            for i in urls:
                                add_url = url_item.UrlItem(i, url.depth + 1)
                                with self.lock:
                                    try:
                                        self.url_queue.put_nowait(add_url)
                                    except Queue.full:
                                        logging.warn("url queue has full, url %s add error" % (add_url.url))
                                        time.sleep(global_value.CRAWL_INTERVAL)
                                        self.url_queue.task_done()

def main():
    Version = "1.0"
    log.init_log("logs/mini_spider")
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(prog='mini_spider')
    parser.add_argument("-c", "--conf", help="config file path", required=True)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + Version)
    args = parser.parse_args()

    try:
        ret_conf = config_load.config_parser(args.conf)
    except UnboundLocalError as msg:
        logging.error("Read conf fail. Message: %s" % msg)
        sys.exit(-1)
    else:
        if ret_conf is False:
            sys.exit(0)

    lock = threading.Lock()
    url_queue = Queue.Queue()
    crawed_urls = set()

    with open(global_value.URL_LIST_FILE) as fp:
        for start_point in fp:
            if not start_point.startswith('http'):
                continue
            start_url = url_item.UrlItem(start_point.strip('/\n\r'))
            url_queue.put(start_url)

    threads = []

    for i in xrange(global_value.THREAD_COUNT):
        spider_thread = SpiderThread(url_queue, lock, crawed_urls)
        threads.append(spider_thread)
        spider_thread.start()
        logging.info("starting spider thread...")

        for thread in threads:
            thread.join()
        logging.info("spider work is done!")

if __name__ == "__main__":
    main()
    



                        
