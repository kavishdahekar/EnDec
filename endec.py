#simple custom encryption decryption

from pyDes import *
from easygui import *
from sys import argv

# script, mode = argv

	
msg = "I'm only offering you the truth, nothing more?"
title = "Choose Neo"
if boolbox(msg, title, ["Red Pill", "Blue Pill"]):
	mode = "encr"
else:
	mode = "decr"

file_path = fileopenbox()
file = open(file_path)
file_contents = file.read()
print file_contents