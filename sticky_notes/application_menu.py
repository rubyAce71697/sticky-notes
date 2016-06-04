#!usr/bin/env python

from stickies import Revealer_Glade
from gi.repository import Gtk,GObject,Gdk,GtkSource
from gi.repository import Pango
from gi.repository import AppIndicator3 as appindicator

from os.path import expanduser
import glob
import os



""" configuration for storing the settings like color, position for ch note according to the uuid """
import ConfigParser

""" importing uuid for the unique id for notes """
import uuid

from configuration import Configurations
import re
import webbrowser

""" learning logging"""
import logging
logging.basicConfig(level = logging.CRITICAL)
logger = logging.getLogger(__name__)

home = expanduser("~")


class Application_Menu:

    notes_uuid = []
    notes_gtk_object = []

    def create_note(self,widget,note = None):
        print note
        if note is not None:
            print "here"

            note = Revealer_Glade(widget,note)

            

        else:
            note = Revealer_Glade(widget,path=None)


        self.add_notes_to_menu(note, widget.get_parent() )

    def __init__(self):
        indicator = appindicator.Indicator.new("Stickies",
                                               "stickies",
                                               appindicator.IndicatorCategory.APPLICATION_STATUS)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        #indicator.set_icon
        menu = Gtk.Menu()

        create_item = Gtk.MenuItem("New Note")
        create_item.connect("activate",self.create_note)

        show_item = Gtk.MenuItem("Notes")
        note_items = Gtk.Menu()
        show_item.set_submenu(note_items)


        show_notes = Gtk.MenuItem("Show All")

        show_notes.connect("activate",self.show_all_notes)
        menu.append(show_notes)
        show_notes.show()

        hide_notes = Gtk.MenuItem("Hide All")
        hide_notes.connect("activate",self.hide_all_notes)
        menu.append(hide_notes)
        hide_notes.show()



        about_item = Gtk.MenuItem("About")
        about_item.connect("activate",self.about_stickies)
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate",self.quit_application)
        menu.append(create_item)
        menu.append(show_item)
        menu.append(about_item)
        menu.append(quit_item)

        indicator.set_menu(menu)
        create_item.show()
        show_item.show()
        about_item.show()
        quit_item.show()

        self.initialize_notes(create_item)


    def add_notes_to_menu(self, note, menu):
        label = ""
        print note
        if note.title:
            logger.debug("note.title is set")
            label = note.title
        else:
            label = str(note.uuid)
            logger.debug("title not set")



        note_gtk_item =  Gtk.MenuItem(label)
        note_gtk_item.connect("activate",self.note_clicked)
        print(menu.get_children()[3].get_label())
        menu.get_children()[3].get_submenu().append(note_gtk_item)
        note_gtk_item.show();

    
    def note_clicked(self,widget):

        for i in Revealer_Glade.notes_list:

            if str(i.uuid) == widget.get_label() or i.title == widget.get_label():
                i.window.set_keep_above(True)
                i.window.set_keep_above(False)

    



    def initialize_notes(self,menu):


        logger.info("Initialising path-- " + home + "/.stickies-data/*.txt")

        logger.debug(glob.glob(home + "/.stickies-data/*.txt"))
        #print glob.glob(home + "/stickies-data/*.txt")
        list = glob.glob(home + "/.stickies-data/*.txt")
        print list
        if list:
            for note in list:
                print note
                self.create_note(menu,note)
        else:
            self.create_note(menu,None)
        logger.info("Starting Gtk loop")
        if menu is not None:
            Gtk.main()


    def show_all_notes(self,widget):

        if not Revealer_Glade.notes_list:
            self.initialize_notes(None)
        else:
            for i in Revealer_Glade.notes_list:
                i.window.show()
                i.window.set_keep_above(True)
                i.window.set_keep_above(False)

    def hide_all_notes(self,widget):


        for i in Revealer_Glade.notes_list:
            i.save_sticky()
            i.window.close()

        Revealer_Glade.notes_list = []

    def about_stickies(self,widget):
        dialog = Gtk.AboutDialog.new()
        # fixes the "mapped without transient parent" warning
        dialog.set_transient_for(widget.get_parent().get_parent())

        dialog.set_program_name("Stickies")
        dialog.add_credit_section("Authors:", ['Nishant Kukreja (github.com/rubyace71697)'])
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_website("https://github.com/rubyAce71697/sticky-notes")
        dialog.set_website_label("Github Page")
        dialog.set_comments("Utility for ubuntu (inspired from stickies for mac)")
        dialog.set_logo_icon_name(os.path.dirname(os.path.abspath(__file__)) +"/stickies.png")
        print os.path.dirname(os.path.abspath(__file__)) + "/stickies.png"

        dialog.run()
        dialog.destroy()


    def quit_application(self,widget):
        for note in Revealer_Glade.notes_list:
            note.save_sticky()


        Gtk.main_quit()





  


def run():
    logger.debug("Running Srickies")
    d = os.path.join(expanduser('~') +  "/.stickies-data")
    print d
    if not os.path.exists(d):
        logger.debug("Creating .stickies-data in home directory")
        os.makedirs(d)

    Application_Menu()



if __name__ == "__main__":

    #initialize_notes(None)Application_Menu()
    print ("use 'sticky_notes' to run ")
