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
					else self.is_sleep += 1
						
