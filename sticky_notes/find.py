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
        self.find_window = self.builder.get_object("find_window")
        self.__search_entry = self.builder.get_object('searchentry1')
        self.find_window.set_can_focus(True)
        self.find_window.connect('delete_event',self.hide)

        

    def show(self):

        logger.debug("Showing the FIND window")

        logger.debug(self.find_window)
        
        GObject.idle_add(self.find_window.grab_focus)
        GObject.idle_add(self.__search_entry.grab_focus)
        GObject.idle_add(self.find_window.show)
        GObject.idle_add(self.find_window.set_keep_above,True)
        

        GObject.idle_add(self.find_window.set_keep_above,False)
       


    def hide(self,widget,event):
        logger.debug("Hiding the get_object")
        GObject.idle_add(widget.hide)

        return True






