import subprocess

print "*"*10 + " Uninstalling Sticky Notes " + "*"*10

#subprocess.call('echo "nishant" | sudo pip uninstall sticky-notes -y')

subprocess.call("python setup.py sdist")

subprocess.call(' echo "nishant" | sudo pip install  ./dist/sticky-notes-2.1.2.tar.gz ')