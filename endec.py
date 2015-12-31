#!/usr/bin/python

from pyDes import *
from easygui import *
from sys import argv
import base64

mode = -1 # operation mode. 0 = encrypt, 1 = decrypt
passkey_len = 8 #default passkey length for DES in bytes
encryption_algo = "TDES" #default encryption, can also use TDES for triple DES

# initial choice box strings
choicebox_mode_choice_msg = "Choose operation mode..."
choicebox_mode_choice_title = "Make a choice"
choicebox_mode_choice_button1 = "Encrypt"
choicebox_mode_choice_button2 = "Decrypt"

# write to file choice box strings
choicebox_write_to_file_msg = "Overwrite file with output?"
choicebox_write_to_file_title = "Make a choice"
choicebox_write_to_file_button1 = "Yes"
choicebox_write_to_file_button2 = "No"

try:
	if argv[1] == "help":
		print "Usage : python endec.py MODE"
		print "MODES : DES(default), TDES"
		print "Example : python endec.py TDES"
	encryption_algo = argv[1]
except IndexError:  
   #doing nothing
   pass

if encryption_algo == "TDES":
	passkey_len = 16

# DES expects fixed length passkeys. This method will digest the passkey to get it to appropriate length
def digest_passkey(passkey):
	passkey_temp = [0]*passkey_len
	for i,c in enumerate(passkey):
		index = i%passkey_len
		passkey_temp[index] = 97 + (passkey_temp[index] + ord(c))%26
	print "Digested passkey : "+str(''.join(chr(c) for c in passkey_temp))
	return ''.join(chr(c) for c in passkey_temp)

def encrypt(secret_text,passkey):
	print "Encryting input with passkey "+str(passkey)+" using "+str(encryption_algo)
	if encryption_algo == "DES":
		return des(digest_passkey(passkey)).encrypt(secret_text, padmode=PAD_PKCS5)
	elif encryption_algo == "TDES":
		return triple_des(digest_passkey(passkey)).encrypt(secret_text, padmode=PAD_PKCS5)

def decrypt(cipher_text,passkey):
	print "Decryting input with passkey "+str(passkey)+" using "+str(encryption_algo)
	try:
		cipher_text = base64.b64decode(cipher_text)
		if encryption_algo == "DES":
			return des(digest_passkey(passkey)).decrypt(cipher_text, padmode=PAD_PKCS5)
		elif encryption_algo == "TDES":
			return triple_des(digest_passkey(passkey)).decrypt(cipher_text, padmode=PAD_PKCS5)
	except ValueError:
		msgbox("Error : encrypted data seems to be corrupted!")
		print "Error : encrypted data seems to be corrupted!"
		sys.exit()

	
# Simplegui has no way to handle close  event of box. So if user closes this box, mode will be set to 1 i.e. decrypt
if boolbox(choicebox_mode_choice_msg, choicebox_mode_choice_title, [choicebox_mode_choice_button1, choicebox_mode_choice_button2]):
	mode = 0 #encrytion
else:
	mode = 1 #decryption

file_path = fileopenbox()
try:
	passfile = open(file_path, "r+")
except IOError:
	msgbox("Unable to open file.")
	sys.exit()
file_contents = passfile.read()

passkey = passwordbox(msg='Enter passkey...', title='Passkey', default='')

endec_mode = {
			0: encrypt,
			1: decrypt
		}

# Calling the function
processed_file_contents = str(endec_mode[mode](file_contents,passkey))

# Display output
textbox("Output", text=processed_file_contents)

# Ask whether to write to file or not
if boolbox(choicebox_write_to_file_msg, choicebox_write_to_file_title, [choicebox_write_to_file_button1, choicebox_write_to_file_button2]):
	if mode == 0:
		processed_file_contents = base64.b64encode(processed_file_contents)
	passfile.seek(0)
	passfile.write(processed_file_contents)
	passfile.truncate()
	passfile.close()
	msgbox("Output written to file!")
else:
	msgbox("Output not written to file!")