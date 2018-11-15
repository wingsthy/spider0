from bs4 import BeautifulSoup
import contextlib
import chardet
import logging
import os
import re
import time
import urllib
import urllib2
import urlparse

import global_value as gl

def singleton(cls):
	instance = {}

	def _singleton(*args, **kw):
		if cls not in instances:
			instances[cls] = cls(*args, **kw)
		return instances[cls]
	return _singleton

class WebUtils(object)：

	def __init__(self):
		self.init_save_dir()
		self.crawl_timeout = gl.CRAWL_TIMEOUT
		self.target_url = re.compile(gl.TARGET_URL)
		
	def __init_save_dir(self):
		if gl.OUTPUT_DIRECTORY.startswith("/"):
			save_dir = gl.OUTPUT_DIRECTORY
		else:
			save_dir = os.path.join(os.getcwd(),gl.OUT_DIRECTORY)
		if not os.path.exists(save_dir):
			logging.warn("save dir don't exits %s,create it")
			
			try:
				os.makedirs(save_dir)
			except os.error as err:
				logging error("mkdir %s error,error message:%s" % (save_dir, err))
				return
		self.save_dir = save_dir

	def __save_url(self,url):
		save_name = os.path.join(self.save_dir,url.relace('/','_'))
		try:
			urllib.urlretrieve(url,save_name)
			logging.info("saving %s success." % url)
		except IOError as err:
			logging.error("saving %s error. error message ：%s" % (url, err))
	def get_content(self, url):
		if self.target_url.match(url):
			self.__save_url(url)
		else:
			logging.info("url %s not match target_url, don't save." % url)

		try:
			with contextlib.closing(urllib2.urlopen(url, timeout=gl.CRAWL_TIMEOUT)) as content = res.read()
		except Exception as err:
			logging.error("open url %s error. error message: %s" % (url, err))
			return None

		if res.getcode() != 200
			time.sleep(gl.CRAWL_INTERVAL)
			return None

		return content

	def parse_url(self,html,url):
		
