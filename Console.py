#
# Console.py
# Advanced console capabilites on Windows
#
# Jonatan H Sundqvist
# July 30 2014
#

# TODO | - Look for portable solutions, dependency checks (cf. curses)
#		 - Decide on API argument scheme (X, Y, tuple, complex, either or, etc)
#		 	-- Decorator for overloads (?)
#		 - Proper Unicode handling, encoding queries
#		 - Saving output
#		 - Sort methods in a logical order (High-level API, Low-level API, internal methods, auxiliary internal methods, etc.)

# SPEC | - 
#		 -


import tkinter as tk

from ctypes import *
from itertools import cycle, takewhile

from sys import stdout
from time import sleep
from random import choice
from collections import namedtuple

if __name__ == '__main__':
	from WinTypes import *
else:
	from WinTypes import *	# (?) # TODO: Fix import error (different behaviour when including this module from another script) (✓)
# from constants import * 	# (?)


class Colours:
	BLACK 	= 0x0
	BLUE 	= 0x1
	GREEN 	= 0x2
	CYAN 	= 0x3
	BLOOD 	= 0x4
	PURPLE 	= 0x5
	GOLD 	= 0x6
	BONE 	= 0x7
	GREY 	= 0x8
	OCEAN 	= 0x9
	GRASS 	= 0xA
	LAGOON 	= 0xB
	RED 	= 0xC
	PINK 	= 0xD
	YELLOW 	= 0xE
	WHITE 	= 0xF


class Console():

	'''
	Wraps the console API for Windows,
	providing a simple interface for 
	advanced text-based interaction.

	'''

	def __init__(self):

		''' '''

		# Acquire handle
		windll.Kernel32.GetStdHandle.restype = c_ulong
		self.HANDLE = c_ulong(0XFFFFFFF5)
		self.hStdout = windll.Kernel32.GetStdHandle(self.HANDLE)

		# Initialize
		self.title('Labyrinthian')

		# Initialize colours
		self.bg = 0x00 # Highest bits indicate bg?
		self.fg = 0x00 # Lowest bits indicate fg?

		# Initialize buffer attributes
		# TODO: Cursor object (eg. pos, visible, etc.) (?)
		self.size 	= None # Buffer size (in characters)
		self.pos 	= 0, 0 # Cursor position (character offset from top left corner)

		self.updateBufferInfo()


	def colour(self, bg=None, fg=None):

		''' Returns or sets foreground and background colour '''

		if (bg is None) and (fg is None):
			return (self.bg << 4) + (self.fg)
		
		if bg is not None:
			assert isinstance(bg, int) and (0x0 <= bg <= 0xF)
			self.bg = bg
		
		if fg is not None:
			assert isinstance(fg, int) and (0x0 <= fg <= 0xF)
			self.fg = fg

		windll.Kernel32.SetConsoleTextAttribute(self.hStdout, (self.bg << 4) + (self.fg))


	def cursor(self, x=None, y=None):

		''' Sets or retrieves the cursor position '''

		self.updateBufferInfo()
		stdout.flush()
		#print('X: %d\n%sY: %d' % (self.pos[0], ' ' * (self.pos[0]), self.pos[1]))
		
		if x is None and y is None:
			# TODO: Make sure self.pos is up to date (cf. print)
			return self.pos

		if x is not None:
			self.pos = x, self.pos[1]

		if y is not None:
			self.pos = self.pos[0], y

		windll.Kernel32.SetConsoleCursorPosition(self.hStdout, COORD(*self.pos))


	def charAt(self, X, Y, char=None, bg=None, fg=None):

		''' Sets or retrieves the character at the specified position '''

		# TODO: Retrieve colour data as well (cf. CHAR_INFO)
		if char is None:
			return 0 # Char at X,Y
		else:
			raise NotImplementedError # Set char at X, Y


	def view(self, section, contents=None, bg=None, fg=None):

		''' Sets or retrieves a rectangular section of the console buffer '''

		raise NotImplementedError


	def updateBufferInfo(self):

		''' '''

		info = BUFFERINFO()
		windll.Kernel32.GetConsoleScreenBufferInfo(self.hStdout, byref(info)) # TODO: Make sure this is correct
		
		self.pos 	= (info.dwCursorPosition.X, info.dwCursorPosition.Y)
		assert self.pos == (info.dwCursorPosition.X, info.dwCursorPosition.Y)
		self.size 	= info.dwSize.X, info.dwSize.Y


	def pullEvent(self):

		''' '''

		raise NotImplementedError

		numEvents = DWORD(0)
		windll.Kernel32.GetNumberOfConsoleInputEvents(self.hStdout, byref(numEvents))
		record = INPUT_RECORD()
		length = DWORD(1)
		windll.Kernel32.GetConsoleScreenBufferInfo(self.hStdout)


	def title(self, title=None):

		''' Returns or sets title '''

		if title is None:
			return self.title
		else:
			self.title = title
			windll.Kernel32.SetConsoleTitleW(title)


	def moveCursor(self, x, y):

		''' Moves the cursor relative to its current position '''

		self.cursor(x+self.pos[0], y+self.pos[1])


	def putTokens(self, *tokens):

		''' '''

		for token in tokens:
			if isinstance(token, str):
				print(token, end=' ')
			else:
				stdout.flush() # Have to flush the buffer for the colour change to take effect. Printing a newline also works.
				self.colour(fg=token)


	def colourPrint(self, string):
		tokens = [word if not hasattr(Colours, word) else getattr(Colours, word) for word in string.split()]
		self.putTokens(*tokens)


	def parseMarkup(self, markup):

		''' '''

		# TODO: Parse markup
		# TODO: Escapes for syntactic characters
		# TODO: Default formatting for plain text
		# TODO: Debugging, error handling
		# TODO: Optimise, extract setup code (eg. definitions)
		# TODO: Use regex or library (?)
		# NOTE: Nested tags are currently not supported
		
		Token = namedtuple('Token', 'fg bg text')
		tokens = []

		# Default values for attributes
		defaults = {
			'fg': 'WHITE',
			'bg': 'BLACK'
		}

		def colour(prop, frmt):
			''' '''
			# TODO: Find a more general name (eg. parseAttributes)
			# TODO: Allow customisation via kwargs (?)
			if prop not in frmt:
				return defaults[prop]
			else:
				# TODO: Use colour aliases when printing tokens (?)
				# TODO: More attributes (...)
				# This sub-parser only consumes upper-case letters (since it's trying to extract a Colour constant)
				#return getattr(Colours, ''.join(takewhile(lambda c: c.isupper(), frmt[frmt.index(prop)+3:])))
				# This generalised sub-parser extracts ANY value token and leaves the interpretation to the caller
				# NOTE: Assumes the delimiter is a space. Easily customised.
				return ''.join(takewhile(lambda c: c not in ' >', frmt[frmt.index(prop)+3:]))

		
		while len(markup) > 0:
			if markup.startswith('<'):
				begin 	= markup.index('<') # Should always be 0 within this branch
				end 	= markup.index('>') # Last index of formatting tag
				frmt 	= markup[begin+1:end]

				close 	= end + 1 + markup[end+1:].index('</>') # Skip formatting tag when looking for closing tag (unnecessary optimization (?))
				text 	= markup[end+1:close]					# Extract text between formatting tag and end tag

				markup  = markup[close+len('</>'):] # Increment the pointer (so to speak)

				# TODO: Use takeWhile or regex (?)
				#fg = Colours.WHITE if 'fg=' not in frmt else getattr(Colours, frmt[]) # TODO: Allow hex colours too (?)
				#bg = Colours.BLACK if 'bg=' not in frmt else getattr(Colours, frmt[frmt.index('bg=')+3:(frmt[frmt.index('bg=')+3:].index())])
				fg  = colour('fg', frmt)
				bg  = colour('bg', frmt)
				tokens.append(Token(fg, bg, text))
			else:
				# Token does not have tags
				end = markup.index('<') if '<' in markup else len(markup)
				tokens.append(Token(defaults['fg'], defaults['bg'], markup[:end]))
				markup = markup[end:]

		return tokens
		#return '<fg=#FC bg=GREEN>Hello there</>This is white text. <fg=RED>IMPORTANT!</>'


	def printMarkup(self, markup):
		
		''' '''
		# NOTE: Currently incompatible with customised markup
		for token in self.parseMarkup(markup):
			self.putColoured(char=token.text, fg=getattr(Colours, token.fg), bg=getattr(Colours,token.bg))

		# TODO: Reset formatting afterwards (?)


	def putColoured(self, char, fg=None, bg=None):
		''' Prints a coloured string '''
		# TODO: Rename char argument
		stdout.flush()
		self.colour(bg=bg, fg=fg)
		print(char, end='')
		stdout.flush()



def main():

	console = Console()

	console.colourPrint('RED ERROR! WHITE ! Two minutes to self destruction.')
	print()
	console.colourPrint('Evacuate GREEN premises WHITE immediately!')
	
	#print(('#'*20+'\n')*20)
	#x = console.cursor(6,5)
	#print('█')
	#x = console.cursor(6,6)
	#print('█')

	print()

	maze = [
		'███████████████████████████████',
		'█       █                     █',
		'█       █                     █',
		'█       █                     █',
		'█       █      █              █',
		'█       █      █              █',
		'█       █      █              █',
		'█              █              █',
		'█              █████████      █',
		'█              █              █',
		'█              █              █',
		'█       ████████              █',
		'█              █              █',
		'█              █              █',
		'█                       █     █',
		'█                       █     █',
		'█                       █     █',
		'███████████████████████████████'
	]

	blocks = {
	 '█': Colours.GREY,
	 ' ': Colours.GREEN
	}

	for line in maze:
		for tile in line:
			colour = blocks[tile]
			console.putColoured(tile, fg=colour, bg=colour)
		print()

	print()

	console.colour(bg=Colours.GREEN, fg=Colours.WHITE)

	def left(steps):
		return [(-1, 0) for X in range(steps)]

	def right(steps):
		return [(1, 0) for X in range(steps)]

	def up(steps):
		return [(0, -1) for X in range(steps)]

	def down(steps):
		return [(0, 1) for X in range(steps)]

	console.cursor(3, 5)


	#==============================================================================================================
	# Negotiating the maze
	#==============================================================================================================
	# NOTE: Printing affects cursor position
	# TODO: Console should take that into account
	for X, Y in down(6) + right(8) + up(7) + right(6) + down(4) + right(8) + down(6) + left(6) + down(3) + left(8):
		break
		console.cursor(X+console.pos[0], Y+console.pos[1])
		print('O')
		sleep(1/24)
		console.cursor(console.pos[0], console.pos[1])
		print(' ')


	#==============================================================================================================
	# Rotating bar
	#==============================================================================================================
	for f in range(10):
		break
		console.cursor(5,5)
		print('|/-\\|/-\\'[f%8])
		console.cursor(7,12)
		print('|/-\\|/-\\'[f%8])
		console.cursor(6,14)
		print('|/-\\|/-\\'[f%8])
		sleep(1/8)


	#==============================================================================================================
	# Animating coloured squares
	#==============================================================================================================
	for f, p, c in zip(range(100), cycle([(5,5), (6,5), (6,6), (5,6)]), cycle([Colours.YELLOW, Colours.PURPLE, Colours.GOLD, Colours.BLOOD])):
		break
		console.cursor(*p)
		console.putColoured(' ', bg=c)
		
		console.cursor(34, 2)
		console.putColoured('Frame: %d' % f, bg=Colours.BLACK)
		console.cursor(34, 4)
		console.putColoured('X: ', bg=Colours.BLACK, fg=Colours.BLOOD)
		console.putColoured(p[0], bg=Colours.BLACK, fg=Colours.WHITE)
		console.putColoured(', Y: ', bg=Colours.BLACK, fg=Colours.OCEAN)
		console.putColoured(p[1], bg=Colours.BLACK, fg=Colours.WHITE)

		sleep(1/5)

		console.cursor(*p)
		console.putColoured(' ', bg=Colours.GREEN)

	console.cursor(0,20)


	#==============================================================================================================
	# Markup test
	#==============================================================================================================
	console.printMarkup('<fg=RED bg=YELLOW>Hello there! </>This is white text. <fg=RED>IMPORTANT!</>')


	#==============================================================================================================
	# EVENTS
	#==============================================================================================================
	app = tk.Tk()
	app.bind('<Left>', 	lambda e: [console.moveCursor(-1, 0), console.putColoured(' ', bg=Colours.GRASS)])
	app.bind('<Right>', lambda e: [console.moveCursor(1, 0), console.putColoured(' ', bg=Colours.GRASS)])
	app.bind('<Up>', 	lambda e: [console.moveCursor(0, -1), console.putColoured(' ', bg=Colours.GRASS)])
	app.bind('<Down>', 	lambda e: [console.moveCursor(0, 1), console.putColoured(' ', bg=Colours.GRASS)])
	app.bind('<space>', lambda e: console.putColoured(' ', bg=choice([Colours.RED, Colours.GOLD, Colours.LAGOON])))
	app.mainloop()


if __name__ == '__main__':
	main()