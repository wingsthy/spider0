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
        char_dict = char_dict["encoding"]
        if web_encoding == 'utf-8' or web_coding == 'UTF-8':
            content = html
        else:
            try:
                content = html.decode('GBK', 'ignore').encode('utf-8')
            except UnicodeDecodeError as err:
                logging.error("decode html error. error message: %s.", err)
                return None
            page_links = []
            base_url = url.strip('/ ')
            try:
                urls = BeautifulSoup(content, "lxml").findAll('a', href=True)
                imgs = BeautifulSoup(content, "lxml").finaAll('img', src=True)
            except TypeError as msg:
                logging.error("Unicode decode error! error message: %s" % msg)
                return page_links

            links_set = set()
            for link in urls:
                if not link['href'].startwith('javascript:'):
                    links_set.add(link['href'])
            for link in imgs:
                links_set.add(link['src'])
            for link in links_set:
                if not link.startwith('http'):
                    try:
                        page_links.append(urlparse.urljoin(base_url, link.strip('/ ')))
                    except UnicodeDecodeError as msg:
                        logging.error('url parse error. error message %s' % msg)
                else:
                    page_links.append(link.strip('/ '))
            return page_links
            
            
