#!usr/bin/env python

import sys
import json
import gi.repository

from gi.repository import Gtk,GObject,Gdk,GtkSource
from gi.repository import Pango
from gi.repository import AppIndicator3 as appindicator

from os.path import expanduser
import glob
import os


""" we will remove it later"""
import ConfigParser

import re


""" yet learning login """
import logging
logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)


home = expanduser('~')




class Find:
    """
    
    TODO: Declare handlers



    """
    def __init__(self):


        logger.debug(" Initializing the FIND object")
        self.builder = Gtk.Builder()
        d = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        #print d
        d = os.path.join(d,"find.glade")
        #print d
        self.builder.add_from_file(d)
        self.find_window = None
        

        

    def show(self):

        logger.debug("Showing the FIND window")

        if self.find_window is None:
            self.find_window = self.builder.get_object("find_window")

        self.find_window.show()
       


    def hide(self):

        self.find_window.hide()






