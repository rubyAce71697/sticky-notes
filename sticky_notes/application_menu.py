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
logger.disablesd = True

home = expanduser("~")


class Application_Menu:

    notes_uuid = []
    notes_gtk_object = []

    def create_note(self,widget = None,note = None):
        print note
        if note is not None:
            print "here"

            note = Revealer_Glade(widget,self,note)



        else:
            note = Revealer_Glade(widget, self,path=None)


        self.add_notes_to_menu(note )

    def __init__(self):
        indicator = appindicator.Indicator.new("Stickies",
                                               "stickies",
                                               appindicator.IndicatorCategory.APPLICATION_STATUS)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        #indicator.set_icon
        self.menu = Gtk.Menu()

        create_item = Gtk.MenuItem("New Note")
        create_item.connect("activate",self.create_note)

        show_item = Gtk.MenuItem("Notes")
        note_items = Gtk.Menu()
        show_item.set_submenu(note_items)


        show_notes = Gtk.MenuItem("Show All")

        show_notes.connect("activate",self.show_all_notes)



        hide_notes = Gtk.MenuItem("Hide All")
        hide_notes.connect("activate",self.hide_all_notes)





        about_item = Gtk.MenuItem("About")
        about_item.connect("activate",self.about_stickies)
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate",self.quit_application)
        self.menu.append(create_item)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(show_notes)
        self.menu.append(hide_notes)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(show_item)
        self.menu.append(Gtk.SeparatorMenuItem())
        self.menu.append(about_item)
        self.menu.append(quit_item)

        indicator.set_menu(self.menu)


        for i in self.menu.get_children():
            i.show()

        self.initialize_notes()

        logger.info("Starting Gtk loop")
        if self.menu is not None:
            Gtk.main()

    def add_notes_to_menu(self, note):
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
        print(self.menu.get_children()[5].get_label())
        self.menu.get_children()[5].get_submenu().append(note_gtk_item)
        note_gtk_item.show();

    def remove_deleted_note_from_menu(self,title):
        for i in self.menu.get_children()[5].get_submenu().get_children():
            if title == i.get_label():
                self.menu.get_children()[5].get_submenu().remove(i)
                break

    def change_the_title_of_note_in_menu(self,old_title,new_title):
	print "|||||||||||||||"*20
	print "tile cchanged" + new_title;

        for i in self.menu.get_children()[5].get_submenu().get_children():

            if old_title == i.get_label():
                i.set_label(new_title)

    def note_clicked(self,widget):


        logger.debug(widget.get_label() + " was clicked + it will be shown now")

        for i in Revealer_Glade.notes_list:

            if str(i.uuid) == widget.get_label() or i.title == widget.get_label():
                i.window.show()
                i.move_window()
                i.window.set_keep_above(True)
                i.window.set_keep_above(False)




    def read_backups(self):

        logger.info("Initialising path-- " + home + "/.stickies-data/*.txt")
        logger.debug(glob.glob(home + "/.stickies-data/*.txt"))
        #print glob.glob(home + "/stickies-data/*.txt")
        lst = glob.glob(home + "/.stickies-data/*.txt")

        return lst




    def initialize_notes(self):


        lst = self.read_backups()

        if lst:
            for note in lst:
                print note
                self.create_note(None,note)
        # else:
        #     self.create_note(self.menu,None)

    def show_all_notes(self,widget):

        if not Revealer_Glade.notes_list:
            self.initialize_notes()
        else:
            for i in Revealer_Glade.notes_list:
                i.save_sticky()
                i.window.show()
                i.move_window()
                i.window.set_keep_above(True)
                i.window.set_keep_above(False)

    def hide_all_notes(self,widget):

	
        for i in Revealer_Glade.notes_list:
            i.save_sticky()
            i.window.hide()

        #Revealer_Glade.notes_list = []

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
