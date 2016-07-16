#!/usr/bin/env python2

from distutils.core import setup
import sys
import glob
import os
from os.path import expanduser
home = expanduser("~")

if 'bdist_wheel' in sys.argv:
    raise RuntimeError("This setup.py does not support wheels")

if (sys.version_info[0]*10 + sys.version_info[1]) < 26:
    raise RuntimeError('Sorry, Python < 2.6 is not supported')

setup(
	name             = "sticky-notes",
	version          = "2.2",
	author           = "Nishant Kukreja",
	author_email     = "kukreja34@gmail.com",
        maintainer       = "Nishant Kukreja",
        maintainer_email = "kukreja34@gmail.com",
	description      = "Stick your notes to your desktop (inspired from stickies for Mac)",
	license          = "GPLv3",
	keywords         = "Sticky Notes for Ubuntu",
	url              = "https://github.com/rubyAce71697/sticky-notes",
	packages         = ["sticky_notes"],
    package_data={'sticky_notes': ['./*.glade']},
	data_files       = [(sys.prefix + "/share/icons/hicolor/24x24/apps", glob.glob("icons/*")),
                        (sys.prefix + "/share/applications",["start-sticky-notes.desktop"])],
	scripts          = ["start-sticky-notes"],
	long_description = open("README").read(),
        requires         = ["requests", "gi.repository"],
        classifiers      = [
            'Development Status :: 5 - Production/Stable',
            'Programming Language :: Python',
            'Environment :: X11 Applications :: Gnome',
            'Environment :: X11 Applications :: GTK',
            'Environment :: Web Environment',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: POSIX :: Linux',
            'Topic :: Desktop Environment :: Gnome',
            'Topic :: Internet'
          ]
        )
#os.chmod(home +"/settings.cfg",0o777)
d = os.path.dirname(expanduser('~') +  "/.sticky-notes")
print d
if not os.path.exists(d):
    os.makedirs(d)
print sys.prefix
