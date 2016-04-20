
========================
Sticky Notes for Ubuntu
========================
Stick your notes to your desktop


Features
==========
* Markdown Support
* Links support (ctrl + left click opens link in default browser)
* Collapse/ Expand your notes 
* Delete/ Hide individual notes
* Hide All/ Show All notes at once
* Set the title of match (default title: first 40 characters  of note - shown when note is collapsed)
* Change color of notes
* Formatting Support (currently only bold is supported)


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

From terminal run::

 start-sticky-notes

To run indicator in background ::

 nohup start-sticky-notes &




Screenshots
=============
.. image:: screenshots/application_menu.png
.. image:: screenshots/collapse.png
.. image:: screenshots/context_menu.png
.. image:: screenshots/change_title.png
.. image:: screenshots/delete_or_not.png

Known Issues
==============
* Ony BOLD style works
* formating is not stored i.e. text will be plain next time you open


TODO:
==========
* Develop common window to show all the notes
* show all the notes in app indicator menu
* Add Application Icon in the Dash


=================
WORK IN PROGRESS
=================
