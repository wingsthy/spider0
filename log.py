import logging
import logging.handlers
import os

class ColoredFormatter(logging.Formatter):
	
	def __init__(self,fmt=None,datefmt=None):
		logging.Formatter.__init__(self,fmt,datefmt)

	def format(self,record):
		
