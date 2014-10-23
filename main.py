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

from SwiftUtils import Console


con = Console.Console()


def pronounce(sentence, sounds, root):

	'''
	Docstring goes here

	'''

	prev = 0 # Length of previous sounds (milliseconds)
	ch = pygame.mixer.Channel(0)

	N = 0


	def play(s):
		def schedule():
			nonlocal N
			ch.queue(s)
			con.moveCursor(0,0)
			con.printMarkup(' '.join(word if index != N else '<fg=GREEN>%s</>' % word for index, word in enumerate(sentence.split())))
			N += 1
		return schedule
	

	for word in sentence.lower().split():
		sound = sounds[word]
		root.after(int(prev),  play(sound))
		prev += sound.get_length()*1000


	# for word, sound in zip(sentence.lower().split(), map(lambda w: sounds[w], sentence.lower().split())):
		# print(word)
		# ch.queue(sound)


def main():
	
	'''
	Docstring goes here

	'''

	root = tk.Tk()
	entry = tk.Entry()
	entry.pack()

	entry.bind('<Return>', lambda e: [print('Saying \'%s\'' % entry.get()), pronounce(entry.get(), sounds, root)])

	pygame.init()
	pygame.mixer.init()

	sounds = { splitext(fn)[0] : pygame.mixer.Sound('resources/%s' % fn) for fn in listdir('resources') if splitext(fn)[1] in ['.wav'] }

	# ch = pygame.mixer.Channel(0)

	# ch.play(sounds['lion'])
	# for word in ('in', 'the', 'jungle', 'sleep', 'tonight', 'in'): ch.queue(sounds[word])
	# print(ch.get_queue())
	# root.bind('e', lambda e: sounds['in'].play())
	# root.bind('q', lambda e: sounds['lion'].play())
	# root.bind('w', lambda e: sounds['in'].play())
	# root.bind('e', lambda e: sounds['the'].play())
	# root.bind('r', lambda e: sounds['jungle'].play())
	pronounce("the mighty lion sleep tonight in the jungle", sounds, root)
	root.mainloop()




if __name__ == '__main__':
	main()