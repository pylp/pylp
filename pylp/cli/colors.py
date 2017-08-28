"""

Change the color of the terminal.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import ctypes


# Get the current system
is_win32 = (os.name == "nt")

# If we are on Windows
if is_win32:
	handle = ctypes.windll.kernel32.GetStdHandle(-11)
	last_fg = 7
	last_bg = 0



# Supported foreground colors, ordered by [ansi, win32]
foreground_colors = {
	"default": [39, 7],
	"black": [30, 0],
	"red": [31, 4],
	"green": [32, 2],
	"yellow": [33, 6],
	"blue": [34, 1],
	"magenta": [35, 5],
	"cyan": [36, 3],
	"lightgray": [37, 7],
	"darkgray": [90, 8],
	"lightred": [91, 12],
	"lightgreen": [92, 10],
	"lightyellow": [93, 14],
	"lightblue": [94, 9],
	"lightmagenta": [95, 13],
	"lightcyan": [96, 11],
	"white": [97, 15]
}

# Supported background colors, ordered by [ansi, win32]
background_colors = {
	"default": [49, 0],
	"black": [40, 0],
	"red": [41, 64],
	"green": [42, 32],
	"yellow": [43, 96],
	"blue": [44, 16],
	"magenta": [45, 80],
	"cyan": [46, 48],
	"lightgray": [47, 112],
	"darkgray": [100, 128],
	"lightred": [101, 192],
	"lightgreen": [102, 160],
	"lightyellow": [103, 224],
	"lightblue": [104, 144],
	"lightmagenta": [105, 208],
	"lightcyan": [106, 176],
	"white": [107, 240]
}



# Set the foreground color
def foreground(color):
	if color not in foreground_colors:
		return
	if is_win32:
		last_fg = foreground_colors[color][1]
		set_color_win32(last_fg | last_bg)
	else:
		set_color_ansi(foreground_colors[color][0])


# Set the background color
def background(color):
	if color not in background_colors:
		return
	if is_win32:
		last_bg = background_colors[color][1]
		set_color_win32(last_fg | last_bg)
	else:
		set_color_ansi(background_colors[color][0])



# Set the color of the terminal on Windows
def set_color_win32(color):
	ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)

# Set the color of the terminal on Linux and MacOS
def set_color_ansi(color):
	print("\e[" + str(color) + "m", end='')
