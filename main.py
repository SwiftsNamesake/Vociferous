#
# Vociferous - main.py
# Primitive speech syntesizer
#
# Jonatan H Sundqvist
# October 23 2014
#

# TODO | - Syncing audio files automatically (Dropbox, Airdrop)
#        - Parsing audio files into separate words
#
# SPEC | -
#        -



import tkinter as tk

import pygame
import pygame.mixer

from os import listdir
from os.path import splitext


def pronounce(sentence):
	''' '''
	pass


def main():
	
	'''
	Docstring goes here

	'''

	pygame.init()
	pygame.mixer.init()

	sounds = { splitext(fn)[0] : pygame.mixer.Sound('resources/%s' % fn) for fn in listdir('resources') if splitext(fn)[1] in ['.wav'] }

	sounds['in'].play()



if __name__ == '__main__':
	main()