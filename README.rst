
========================
Sticky Notes for Ubuntu
========================
Stick your notes to your desktop


Features
==========
* Markdown Support
* Links support (ctrl + left click opens link in default browser)
* Links to files are also supported (file:///home/Downloads etc). Links will open in default app.
* Show all your notes in App Indicator, giving access to note on one click.
* Identifier in the App Inidicator is the tile of the note. If the title is not set for note, the either previous title of uuid for note is shown
* Collapse/ Expand your notes
* Delete/ Hide individual notes
* Hide All/ Show All notes at once
* Set the title of match (default title: first 40 characters  of note - shown when note is collapsed)
* Change color of notes (Colours will also show in the indicator and will change once the colour of note is changed)
* Formatting Support (Markdown Supported)
* Expand/ Collapse All notes



Instructions
==================

Install (PyPI)
--------------
::

 sudo pip install -i https://pypi.python.org/pypi sticky-notes

 If icons are not working then use ::
  sudo git-update-icon-cache /usr/share/icons/hicolor

Uninstall
------------
::

 sudo pip uninstall sticky-notes


(Remove Data)
In Home Directory ::

 rm -r .stickies-data
 rm .stickies.cfg



Usage
===================

From Launcher run:
 Sticky Notes

From terminal run::

 start-sticky-notes

To run indicator in background ::

 nohup start-sticky-notes &


Changelog
==============
* Expand All/ Collapse All functionality implemented
* Links to files are supported now.
* Notes Can be access from Application Indicator
* Under Notes Submenu, clicking on menuitems will show their respective notes
* Identifier of Note in App Indicator is updated as soon as the it is updated for the note.
* If the tile of tou note is not set then the old title/ uuid of the note is shown as Identifier in the App Indicator
* Window position between "Hide All" and "Show All" actions is preserved now
* Added Launcher Icon


Screenshots
=============
.. image:: screenshots/application_menu.png
.. image:: screenshots/new_menu.png
.. image:: screenshots/collapse.png
.. image:: screenshots/context_menu.png
.. image:: screenshots/change_title.png
.. image:: screenshots/delete_or_not.png

Known Issues:
--------------
* Compile View font size is fixed and will be larger according to window1
* Web View Size canot be changed
* Currently User Cannot go back from MarkDown View to text mode

TODO:
==========
* Implement Find All function to search in all the notes and current note
* Implement self arrange functionality (Accoring to created date, color,sorted title(if set) )
