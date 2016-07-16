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




class Revealer_Glade:

    no_of_notes = 0
    notes_list = []


    
    def __init__(self,widget, application_menu_object, path = None):


        handlers = {
            #"on_button1_clicked" : self.on_button1_clicked,
            "on_eventbox1_button_press_event": self.on_eventbox1_button_press_event,
            "destroy" : self.close_sticky,
            "on_toogleminimize_eventbox_button_press_event": self.on_toogleminimize_eventbox_button_press_event,
            "on_close_eventbox_button_press_event": self.close_sticky,
            "on_check_resize_textview": self.on_check_resize_textview,
            "on_colorbutton1_color_activated": self.on_colorbutton1_color_activated,
            "on_colorbutton1_color_set":self.on_colorbutton1_color_set,
            "on_button1_clicked":self.on_button1_clicked,
            "on_textview2_populate_popup":self.on_textview2_populate_popup,
            "on_textview2_motion_notify_event":self.on_textview2_motion_notify_event
        }


        Revealer_Glade.notes_list.append(self)
        logger.debug(Revealer_Glade.notes_list)
        self.config = Configurations()
        self.application_menu_object = application_menu_object
        self.configuration = {}
        self.always_on_top_active = False
        note_string = ""
        self.path = path
        self.title = ""
        if self.path is None:
            print "self.path is none"
            #evealer_Glade.no_of_notes += 1
            self.uuid = uuid.uuid4()
            self.path = home + "/.stickies-data/" + str(self.uuid) +".txt"
            print self.path
        else:
            self.uuid = self.path[-40:-4]
            logger.debug("uid is " +  self.uuid)
            with open(path,'r') as file_to_read:
                print file_to_read
                note_string = file_to_read.read()

            self.configuration = self.config.readConfigurations(str(self.uuid))

        ##widget.get_parent().get_children()[1].get_children().append



        logger.info("Configurations read for uid " + str(self.uuid) if self.uuid else self.uuid)
        logger.debug("Configuration for uid " + str(self.uuid) if self.uuid else self.uuid + "are" + self.configuration)

        self.builder = Gtk.Builder()
        GObject.type_register(GtkSource.View)
        #self.builder.add_from_file( os.path.dirname(os.path.abspath(__file__)) + "/stickies.glade")
        d = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        print d
        d = os.path.join(d,"stickies.glade")
        print d
        self.builder.add_from_file(d)

        self.window = self.builder.get_object("window1")
        self.scrolledwindow = self.builder.get_object("scrolledwindow3")
        self.revealer = self.builder.get_object("revealer2")
        self.textview = self.builder.get_object("textview2")
        self.colorbuttn = self.builder.get_object("colorbutton1")
        self.label = self.builder.get_object("label2")
        self.toogle_label =  self.builder.get_object("toogleminimize")
        self.close_label = self.builder.get_object("close")
        self.textbuffer = self.textview.get_buffer()

        self.title = ""

        language_manager = GtkSource.LanguageManager()
        #logger.debug(language_manager.get_available_languages())
        self.textbuffer.set_language(language_manager.get_language('markdown'))


        self.textbuffer.set_text(note_string)
        self.text_changed(None)
        #self.button = self.builder.get_object("button1")
        #self.label.set_text(str(self.uuid))
        self.printbtn = self.builder.get_object("button1")

        self.tag_list = []
        self.builder.connect_signals(handlers)
        self.textbuffer.connect('changed',self.text_changed)
        self.window.hide()

        if  self.configuration:
            self.bg_color = Gdk.Color(self.configuration['color']['red'], self.configuration['color']['green'], self.configuration['color']['blue'])
            self.title = self.configuration['title']
            self.label.set_text(self.title)
            self.move_window()
            self.revealer.set_reveal_child(self.configuration['reveal'])

        else:
            self.bg_color = Gdk.Color(red=60909, green=54484, blue=0)
            self.title = ""
            self.label.set_text("")




        self.window.modify_bg(Gtk.StateType.NORMAL,self.bg_color)
        self.textview.modify_bg(Gtk.StateType.NORMAL,self.bg_color)
        

        self.save_sticky()

        self.window.show_all()

    def move_window(self):
    	self.window.move(self.configuration['x'],self.configuration['y'])
    	self.save_sticky()

    def text_changed(self,textbuffer):
        GObject.idle_add(self.check_for_urls)

    def check_for_urls(self):

        logger.info('IN CHECK_FOR_URLS')
        self.textbuffer.handler_block_by_func(self.text_changed)
        cursor_position = self.textbuffer.props.cursor_position
        logger.debug(cursor_position)
        if len(self.tag_list) == 1:
            self.tag_list.append(self.textbuffer.create_tag("underline",weight=Pango.Weight.BOLD))

        startiter = self.textbuffer.get_start_iter()
        enditer = self.textbuffer.get_end_iter()
        text = ""
        text = self.textbuffer.get_text(startiter,enditer, include_hidden_chars = True)
        logger.debug(text)
        self.textbuffer.delete(startiter,enditer)

        regex = re.compile(r"(([0-9a-zA-Z]+://\S+)|(www\.\S+))")
        word_list = []



        lines = text.split("\n")
        for i, line in enumerate(lines):

            words_of_line = line.split(" ")

            for w,word in enumerate(words_of_line):
                match = regex.search(word)
                if match:
                    start,end = match.span()
                    self.textbuffer.insert(self.textbuffer.get_end_iter(),word[:start])
                    tag = self.textbuffer.create_tag(None)
                    tag.props.underline = Pango.Underline.SINGLE
                    tag.props.foreground = "#0000FF"
                    #tag.add_events(Gdk.BUTTON_PRESS_MASK)
                    tag.connect("event",self.hyperlink_clicked)

                    tag.url = word[start:end]
                    self.textbuffer.insert_with_tags(self.textbuffer.get_end_iter(),word[start:end],tag)
                    self.textbuffer.insert(self.textbuffer.get_end_iter(),word[end:])

                else:
                    self.textbuffer.insert(self.textbuffer.get_end_iter(),word)

                if w != len(words_of_line)-1:
                    self.textbuffer.insert(self.textbuffer.get_end_iter()," ")


            if i != len(lines)-1:
                logger.debug(i)
                self.textbuffer.insert(self.textbuffer.get_end_iter(),"\n")

        #self.textbuffer.props.cursor_position = cursor_position

        #To change the position of the cursor, call textView.Buffer.PlaceCursor(textView.Buffer.EndIter).

        self.textbuffer.place_cursor(self.textbuffer.get_iter_at_offset(cursor_position))

        self.textbuffer.handler_unblock_by_func(self.text_changed)



    def hyperlink_clicked(self,tag,textview,event,iter):
        #tag.handler_block_by_func(self.hyperlink_clicked)
        print "---------------------------------------------------------------------------"
        #print event.get_state()[1] == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.BUTTON1_MASK
        print event.type
        print "state is printing"
        event.get_state()
        print event.type == Gdk.EventType.BUTTON_RELEASE and event.get_state()[1] == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.BUTTON1_MASK
        print event.type
        print event.get_state()
        print event.state
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.get_state()[1] == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK| Gdk.ModifierType.BUTTON1_MASK :
            logger.debug("Link Left clicked")
            logger.debug(tag.url)
            logger.debug(iter.get_line())
            logger.debug(event)
            logger.debug(iter)
            url = tag.url
            regex = re.compile(r"([0-9a-zA-Z]+://.*)")
            match = regex.search(url)

            if not match:
                logger.debug("url found")
                url = "https://" + url


            webbrowser.open(url,new = 2,autoraise = 2)

           
    def open_in_browser_activated(self,widget,url,tag):

        regex = re.compile(r"([0-9a-zA-Z]+://.*)")
        match = regex.search(url)

        if not match:
            logger.debug("url found")
            url = "https://" + url


        webbrowser.open(url,new = 2,autoraise = 2)
        tag.handler_unblock_by_func(self.hyperlink_clicked)
    def copy_link_activated(self,widget,url,tag):
        tag.handler_unblock_by_func(self.hyperlink_clicked)
        pass





    def go_to_browser(self,widget):
        logger.info("go_to_browser clicked")

    def copy_link(self,widget):
        logger.info("copy_link clicked")


    def on_check_resize_textview(self,widget):
        pass

    def on_colorbutton1_color_activated(self,widget):
        print "it should bbe fired"
        print self.colorbuttn.get_current_color()

    def on_colorbutton1_color_set(self,widget):
        print "now it should work"
        print widget.get_color()
        self.window.modify_bg(Gtk.StateType.NORMAL,widget.get_color())
        self.textview.modify_bg(Gtk.StateType.NORMAL,widget.get_color())

    def bold_clicked(self,widget):
        if not self.tag_list  :
            tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
            tag_underline = self.textbuffer.create_tag("underline", weight=Pango.Weight.UNDERLINE)
            tag_italic = self.textbuffer.create_tag("italic", weight=Pango.Weight.ITALIC)
            self.tag_list.append(tag_bold)
            self.tag_list.append(tag_underline)
            self.tag_list.append(tag_italic)
        if self.textbuffer.get_has_selection():
            self.textbuffer.apply_tag(self.tag_list[0],self.textbuffer.get_selection_bounds()[0],self.textbuffer.get_selection_bounds()[1])

        logger.debug("Bold Clicked")

        print tag_bold
    def underline_clicked(self,widget):
        if not self.tag_list  :
            tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
            tag_underline = self.textbuffer.create_tag("underline", weight=Pango.Weight.UNDERLINE)
            tag_italic = self.textbuffer.create_tag("italic", weight=Pango.Weight.ITALIC)
            self.tag_list.append(tag_bold)
            self.tag_list.append(tag_underline)
            self.tag_list.append(tag_italic)
        if self.textbuffer.get_has_selection():
            self.textbuffer.apply_tag(self.tag_list[1],self.textbuffer.get_selection_bounds()[0],self.textbuffer.get_selection_bounds()[1])

        logger.debug("Underline Clicked")

    def strikethrough_clicked(self,widget):
        if not self.tag_list  :
            tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
            tag_underline = self.textbuffer.create_tag("underline", weight=Pango.Weight.UNDERLINE)
            tag_italic = self.textbuffer.create_tag("italic", weight=Pango.Weight.ITALIC)
            tag_strikethrough = self.textbuffer.create_tag("strikethrough",weight = Pango.Weight.STRIKETHROUGH)
            self.tag_list.append(tag_bold)
            self.tag_list.append(tag_underline)
            self.tag_list.append(tag_italic)
            self.tag_list.append(tag_strikethrough)
        if self.textbuffer.get_has_selection():
            self.textbuffer.apply_tag(self.tag_list[3],self.textbuffer.get_selection_bounds()[0],self.textbuffer.get_selection_bounds()[1])

        logger.debug("Strikethrough Clicked")

    def italic_clicked(self,widget):
        if not self.tag_list  :
            tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
            tag_underline = self.textbuffer.create_tag("underline", weight=Pango.Weight.UNDERLINE)
            tag_italic = self.textbuffer.create_tag("italic", weight=Pango.Weight.ITALIC)
            self.tag_list.append(tag_bold)
            self.tag_list.append(tag_underline)
            self.tag_list.append(tag_italic)
        if self.textbuffer.get_has_selection():
            self.textbuffer.apply_tag(self.tag_list[2],self.textbuffer.get_selection_bounds()[0],self.textbuffer.get_selection_bounds()[1])

        logger.debug("Italic Clicked")

    def textview_color_changed(self,widget):
        logger.debug(widget.get_label() + " clicked")
        if widget.get_label() == "Yellow":
            self.bg_color = Gdk.Color(red=64764, green=59881, blue=20303)
        elif widget.get_label() == "Blue":
            self.bg_color = Gdk.Color(red=29298, green=40863, blue=53199)
        elif widget.get_label() == 'Purple':
            self.bg_color = Gdk.Color(red=44461, green=32639, blue=43176)
        elif widget.get_label() == "Peach":
            self.bg_color = Gdk.Color(red=64764, green=44975, blue=15934)

        self.window.modify_bg(Gtk.StateType.NORMAL,self.bg_color)
        self.textview.modify_bg(Gtk.StateType.NORMAL,self.bg_color)
            
            

    def show_file_chooser(self,widget):

        colorchooserdialog = Gtk.ColorChooserDialog()

        response = colorchooserdialog.run()

        if response == -5:
            # colorsel  = colorchooserdialog.colorsel
            # color = colorsel.get_current_color()
            color = colorchooserdialog.get_rgba()
            self.window.modify_bg(Gtk.StateType.NORMAL,color)
        else:
            pass


        logger.debug(response)
        colorchooserdialog.destroy()

    def always_on_top_clicked(self,widget):
        self.window.set_keep_above(widget.get_active())
        self.always_on_top_active = widget.get_active()





    def on_textview2_populate_popup(self,textview,menu):
        always_on_top = Gtk.CheckMenuItem("Always on Top")
        always_on_top.set_active(self.always_on_top_active)
        bold = Gtk.MenuItem("Bold")
        Italic = Gtk.MenuItem("Italic")
        Underline = Gtk.MenuItem("Underline")
        strikethrough = Gtk.MenuItem("Strikethrough")
        menu.append(always_on_top)
        menu.append(bold)
        menu.append(Italic)
        menu.append(Underline)
        menu.append(strikethrough)
        always_on_top.show()
        bold.show()
        Underline.show()
        strikethrough.show()
        Italic.show()

        always_on_top.connect("activate",self.always_on_top_clicked)
        bold.connect("activate",self.bold_clicked)
        #Underline.connect("activate",self.underline_clicked)
        #strikethrough.connect("activate",self.strikethrough_clicked)
        #Italic.connect("activate",self.strikethrough_clicked)
        change_title = Gtk.MenuItem("Change Title")
        menu.append(change_title)
        change_title.show()

        change_title.connect("activate",self.change_note_title)



        textview_colors = Gtk.MenuItem("Colors")
        menu.append(textview_colors)


        colors_menu = Gtk.Menu()
        textview_colors.set_submenu(colors_menu)






        colors_menu.append(Gtk.MenuItem("Blue"))
        colors_menu.append(Gtk.MenuItem("Purple"))
        colors_menu.append(Gtk.MenuItem("Yellow"))
        colors_menu.append(Gtk.MenuItem("Peach"))
        colors_menu.append(Gtk.MenuItem("White"))
        colors_menu.append(Gtk.MenuItem("More Colors"))

        logger.debug(colors_menu.get_children())

        for menuitem in colors_menu.get_children()[:-2]:
            menuitem.show()
            menuitem.connect("activate",self.textview_color_changed)
        
        #colors_menu.get_children()[-1].show()
        #colors_menu.get_children()[-1].connect("activate",self.show_file_chooser)
        textview_colors.show()

    def get_text(self,parent, message, default=''):
        """
        Display a dialog with a text entry.
        Returns the text, or None if canceled.
        """
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Enter the Title")
        dialog.add_button("CANCEL",Gtk.ButtonsType.CANCEL)

        entry = Gtk.Entry()
        entry.set_text(default)
        entry.show()
        box = dialog.get_content_area()
        box.add(entry)

        entry.connect('activate', lambda _: dialog.response(Gtk.ResponseType.OK))
        dialog.set_default_response(Gtk.ResponseType.OK)

        r = dialog.run()
        text = entry.get_text().decode('utf8')
        dialog.destroy()
        if r == Gtk.ResponseType.OK:
            return text
        else:
            return None

    def change_note_title(self,widget):
        text = self.get_text(self.window,"Enter the Title. ")
        if  len(text):

        	self.application_menu_object.change_the_title_of_note_in_menu(self.title if self.title else str(self.uuid), text)
        	self.title = text
        	self.label.set_text(text)

        else:
            self.title = ""

        logger.debug(text)





    def on_button1_clicked(self,widget):
        if self.textbuffer.get_has_selection():

            logger.info("Text is selected")
            logger.info("Selected Text: " + self.textbuffer.get_text(self.textbuffer.get_selection_bounds()[0],self.textbuffer.get_selection_bounds()[1],include_hidden_chars=True))
            logger.debug(self.textbuffer.get_selection_bounds())

        else:
            logger.info("Text is not selected")

    def on_eventbox1_button_press_event(self,widget,event):
        print self.window.get_size()[1]
        print "This event called"
        print Gdk.Event
        if event.type == 5:
            if self.revealer.get_reveal_child():
                self.revealer.set_reveal_child(False)
                logger.debug(self.window.get_size())

                #self.window.set_size_request(self.window.get_size()[0],15)
                #.window.set_size_request, -1, -1)
                #self.window.resize(self.window.get_size()[0],15)

                logger.info("hiding text view")
                self.revealer.hide()

                #self.textview.set_size_request(self.window.get_size()[0],0)
                self.window.set_size_request(self.window.get_size()[0],15)
                self.window.resize(self.window.get_size()[0],15)
                no_of_lines = self.textbuffer.get_line_count()
                no_of_chars = self.textbuffer.get_char_count()
                startiter = self.textbuffer.get_start_iter()
                enditer = self.textbuffer.get_end_iter()
                logger.debug("Info about note hiding text view")
                logger.debug(no_of_lines)
                logger.debug(no_of_chars)

                logger.debug("---------------------------------------------------------------------------------------")
                logger.debug(self.title)

                if self.title == "":
                    logger.debug("checking title")
                    self.label.set_text((self.textbuffer.get_text(startiter,enditer,include_hidden_chars=False)).split("\n")[0][:40])

                logger.debug(self.label.get_text())
                print self.label.get_text()
                print "contracted"
                self.close_label.hide()
                self.toogle_label.hide()
            else:
                self.revealer.show()
                logger.info("revealing text view")

                if self.title == "":
                    self.label.set_text("")

                self.revealer.set_reveal_child(True)
                self.close_label.show()
                self.toogle_label.show()
        else:
            self.window.begin_move_drag(event.button, event.x_root,
                                        event.y_root, event.get_time())
           


    def on_textview2_motion_notify_event( self, widget, event):
        logger.info("Mouse moving in text view")
        """ used to change cursors pointer when mouse over a link.
        Changed from http://download.gna.org/nfoview/doc/api/nfoview.view_source.html
        as returns False now so we can still select content """
        window = Gtk.TextWindowType.WIDGET
        x, y = widget.window_to_buffer_coords(window, int(event.x), int(event.y))
        logger.debug("cordinates: " + str(x) + " " + str(y))
        window = widget.get_window(Gtk.TextWindowType.TEXT)
        for tag in widget.get_iter_at_location(x, y).get_tags():
            logger.debug(" in loop tag = " + tag.url)
            print event.get_state()
            if hasattr(tag, "url") and event.get_state() == Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD2_MASK:
                logger.debug(" Cordinates have tag url")
                window.set_cursor(Gdk.Cursor(cursor_type=Gdk.CursorType.HAND2))
                return False # to not call the default handler.
        window.set_cursor(Gdk.Cursor(cursor_type=Gdk.CursorType.XTERM))

        return False


    def on_toogleminimize_eventbox_button_press_event(self,widget,event):

        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            logger.debug(self.window.get_size())
            logger.info("HIDING TEXT VIEW")


            self.revealer.hide()

            #self.textview.set_size_request(self.window.get_size()[0],0)
            self.window.set_size_request(self.window.get_size()[0],15)
            self.window.resize(self.window.get_size()[0],15)

        else:
            self.revealer.show()
            logger.info("REVEALING TEXT VIEW")
            self.revealer.set_reveal_child(True)

    def close_sticky(self,widget,event):
        #print "error whille closing windwo"




        self.save_sticky()
        dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, "Do you want to DELETE sticky or not")

        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            os.remove(self.path)
            self.window.close()
            Revealer_Glade.notes_list.remove(self)

            self.application_menu_object.remove_deleted_note_from_menu( self.title if self.title else str(self.uuid))

        self.window.hide()


    def save_sticky(self):

        startiter = self.textbuffer.get_start_iter()
        enditer = self.textbuffer.get_end_iter()




        
        self.configuration['height'],self.configuration['width'] = self.window.get_size()
        self.configuration['x'],self.configuration['y'] = self.window.get_position()
        self.configuration['reveal'] = self.revealer.get_reveal_child()
        self.configuration['title'] = self.title
        self.configuration['color'] = {}
        self.configuration['color']['red'] = self.bg_color.red
        self.configuration['color']['green'] = self.bg_color.green
        self.configuration['color']['blue'] = self.bg_color.blue

        preferences = {}
        preferences['color'] = {}
        preferences['height'],preferences['width'] = self.window.get_size()
        preferences['x'],preferences['y'] = self.window.get_position()
        preferences['reveal'] = self.revealer.get_reveal_child()
        preferences['title'] = self.title
        preferences['color']['red'] = self.bg_color.red
        preferences['color']['green'] = self.bg_color.green
        preferences['color']['blue'] = self.bg_color.blue
        logger.debug("height : " + str(self.window.get_size()[1]))
        logger.debug("height : " + str(self.window.get_size()[0]))
        logger.debug("red : " + str(self.bg_color.red))
        logger.debug("green : " + str(self.bg_color.green))
        logger.debug("blue : " + str(self.bg_color.blue))
        logger.debug(self.path)

        open( self.path,'wb+')
        with open( self.path,'wb+') as note_file:
            note_file.write(self.textbuffer.get_text(startiter,enditer,include_hidden_chars=True))

        logger.debug(self.textbuffer.get_text(startiter,enditer,include_hidden_chars=True))
        self.config.writeConfigurations(str(self.uuid),preferences)




    """
    def on_button1_clicked(self,widget):

        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            GObject.idle_add(self.window.resize,20,10)
        else:
            self.revealer.set_reveal_child(True)
    """











#Gtk.main()
    
