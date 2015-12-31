#simple custom encryption decryption

from pyDes import *
import easygui as gui
from sys import argv

script, mode = argv

file = gui.fileopenbox()
file_contents = file.read()

msg = "I'm only offering you the truth, nothing more?"
	title = "Choose"
	if ccbox(msg, title):     # show a Continue/Cancel dialog
		pass  # user chose Continue
	else:  # user chose Cancel
		sys.exit(0)          
	