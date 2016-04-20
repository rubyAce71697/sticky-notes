import ConfigParser
import os
from os import path
from os.path import expanduser
import logging
import json
logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)


class Configurations:
	home = expanduser('~')
	def __init__(self):
		logger.info("Configurations initialised. Currently it will store only settings and not data")
		self.config = ConfigParser.RawConfigParser()
		#home = os.path.dirname(os.path.abspath(__file__))
		

	def readConfigurations(self,uid):
		#home = os.path.dirname(os.path.abspath(__file__))
		home = expanduser('~')
		print "cfg file: " + home + "/.stickies.cfg"
		with open(home + "/.stickies.cfg",'a'):
			self.config.read(path.join(home,".stickies.cfg"))
		
		if not self.config.has_section(str(uid)):
			logger.info("NO PREFRENCES available for " + str(str(uid)))
			return None

		else:
			preferences = {}
			preferences["reveal"] = self.config.getboolean(str(uid),'reveal')
			preferences['title'] = self.config.get(str(uid),'title')
			preferences['x'] = self.config.getint(str(uid),'x')
			preferences['y'] = self.config.getint(str(uid), 'y')
			preferences["height"] = self.config.getint(str(uid),'height')
			preferences["width"] = self.config.getint(str(uid),'width')
			preferences['color'] = {}
			preferences['color']['red'] = self.config.getint(str(uid),'red')
			preferences['color']['green'] = self.config.getint(str(uid),'green')
			preferences['color']['blue'] = self.config.getint(str(uid),'blue')
			logger.info("preferences read for str(uid) " + str(uid))
			logger.debug("PREFERENCES for str(uid) " + str(uid) + "are" + json.dumps(preferences))

			return preferences



	def writeConfigurations(self,uid,preferences=None):

		home = expanduser('~')
		self.config.read(path.join(home,".stickies.cfg"))
		
		if not self.config.has_section(str(uid)):
			logger.info("Section for uid " + str(uid) + "added")
			self.config.add_section(str(uid))
		if not preferences:
			logger.info("NO PREFERENCES for uid" + str(uid) + "were sent")

			
		else:

			self.config.set(str(uid),"height",preferences['height'])
			self.config.set(str(uid),"width",preferences['width'])
			self.config.set(str(uid),'reveal',preferences['reveal'])
			self.config.set(str(uid),'title',preferences['title'])
			self.config.set(str(uid),'x',preferences['x'])
			self.config.set(str(uid),'y', preferences['y'])
			self.config.set(str(uid),"red",preferences['color']['red'])
			self.config.set(str(uid),"green",preferences['color']['green'])
			self.config.set(str(uid),"blue",preferences['color']['blue'])

		with open(path.join(home,".stickies.cfg"),"wb+") as configfile:
			self.config.write(configfile)

		logger.info("PREFERENCES for str(uid) " + str(uid) +" were written to config ")
		logger.debug("PREFERENCES for str(uid) " + str(uid) + "were written")



		
