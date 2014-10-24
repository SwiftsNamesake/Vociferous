#
# WinTypes.py
# Defines argument types and aliases
#
# Jonatan H Sundqvist
# July 31 2014
#

# TODO | - 
#		 - 

# SPEC | - 
#		 -


from ctypes import *


# Typedefs
WORD 	= c_ushort 	# short
DWORD 	= c_ulong	# unsigned long
CHAR 	= c_char	# char
WCHAR 	= c_wchar	# wchar_t
DOUBLE 	= c_double	# double
FLOAT 	= c_float	# float
SHORT 	= c_short	# short
BOOL 	= c_int		# int
UINT 	= c_uint	# unsigned int


# Structures and unions
class COORD(Structure):
	_fields_ = [('X', c_short), ('Y', c_short)]


class SMALL_RECT(Structure):
	_fields_ = [('Left', SHORT), ('Top', SHORT), ('Right', SHORT), ('Bottom', SHORT)]


class BUFFERINFO(Structure):
	_fields_ = [('dwSize', 				COORD),
				('dwCursorPosition', 	COORD),
				('wAttributes', 		WORD),
				('srWindow', 			SMALL_RECT),
				('dwMaximumWindowSize', COORD)]


class uChar(Union):
	_fields = [('UnicodeChar', WCHAR), ('AsciiChar', CHAR)]


class KEY_EVENT_RECORD(Structure):
	_fields_ = [('bKeyDown', BOOL),
				('wRepeatCount', WORD),
				('wVirtualKeyCode', WORD),
				('wVirtualScanCode', WORD),
				('uChar', uChar),
				('dwControlKeyState', DWORD)]


class MOUSE_EVENT_RECORD(Structure):
	_fields_ = [('dwMousePosition', COORD),
				('dwButtonState', DWORD),
				('dwControlKeyState', DWORD),
				('dwEventFlags', DWORD)]


class WINDOW_BUFFER_SIZE_RECORD(Structure):
	_fields_ = [('dwSize', COORD)]


class MENU_EVENT_RECORD(Structure):
	_fields = [('dwCommandId', UINT)]


class FOCUS_EVENT_RECORD(Structure):
	_fields_ = [('bSetFocus', BOOL)]


class Event(Union):
	_fields_ = [( 'KeyEvent', KEY_EVENT_RECORD),
    			( 'MouseEvent', MOUSE_EVENT_RECORD),
    			( 'WindowBufferSizeEvent', WINDOW_BUFFER_SIZE_RECORD),
    			( 'MenuEvent', MENU_EVENT_RECORD),
    			( 'FocusEvent', FOCUS_EVENT_RECORD)]


class INPUT_RECORD(Structure):
	_fields_ = [('EventType', WORD), ('Event', Event)]

	# TODO: Extract these constants (?)
	FOCUS_EVENT = DWORD(0x0010)
	KEY_EVENT 	= DWORD(0x0001)
	MENU_EVENT 	= DWORD(0x0008)
	MOUSE_EVENT = DWORD(0x0002)
	WIDNOW_BUFFER_SIZE_EVENT = DWORD(0x0004)


class CHAR_INFO(Structure):
	_fields_ = [('Char', uChar), ('Attributes', WORD)]