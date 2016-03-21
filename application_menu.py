
import gi.repository
from gi.repository import Gtk,GObject,Gdk

from gi.repository import AppIndicator3 as appindicator
#from revealer_glade import create_note
import os
import os.path

class Application_Menu:

	def __init__(self):

		indicator = appindicator.Indicator.new("Stickies",
		os.path.dirname(os.path.abspath(__file__)) +"/stickies.png",
			appindicator.IndicatorCategory.APPLICATION_STATUS)
		indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		#indicator.set_icon
		menu = Gtk.Menu()

		add_item = Gtk.MenuItem("New Note")
		add_item.connect("activate",create_note)
		
		show_item = Gtk.MenuItem("Notes")
		note_items = Gtk.Menu()
		note_1 = Gtk.MenuItem("Note 1")
		note_items.append(note_1)
		show_item.set_submenu(note_items)





		about_item = Gtk.MenuItem("About")
		about_item.connect("activate",about_stickies)
		quit_item = Gtk.MenuItem("Quit")
		quit_item.connect("activate",Gtk.main_quit)
		menu.append(add_item)
		menu.append(show_item)
		menu.append(about_item)
		menu.append(quit_item)

		indicator.set_menu(menu)
		add_item.show()
		show_item.show()
		note_1.show()
		about_item.show()
		quit_item.show()

def create_note(widget, note = None):
	print note
	if note is not None:
		print "here"
		Revealer_Glade(note)
		#GObject.idle_add(Revealer_Glade(note))
	else:
		Revealer_Glade()
	
def about_stickies(widget):
    dialog = Gtk.AboutDialog.new()
    # fixes the "mapped without transient parent" warning
    dialog.set_transient_for(widget.get_parent().get_parent())

    dialog.set_program_name("Stickies")
    dialog.add_credit_section("Authors:", ['Nishant Kukreja (github.com/rubyace71697)'])
    dialog.set_license_type(Gtk.License.GPL_3_0)
    dialog.set_website("website to be added")
    dialog.set_website_label("Site not available")
    dialog.set_comments("Utility for ubuntu (inspired from stickies for mac)")
    dialog.set_logo_icon_name(os.path.dirname(os.path.abspath(__file__)) +"/stickies.png")
    print os.path.dirname(os.path.abspath(__file__)) + "/stickies.png"

    dialog.run()
    dialog.destroy()



