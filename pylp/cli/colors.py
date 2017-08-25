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
	"light-gray": [37, 7],
	"dark-gray": [90, 8],
	"light-red": [91, 12],
	"light-green": [92, 10],
	"light-yellow": [93, 14],
	"light-blue": [94, 9],
	"light-magenta": [95, 13],
	"light-cyan": [96, 11],
	"white": [97, 15]
}

# Supported background colors, with [ansi, win32]
background_colors = {
	"default": [49, 0],
	"black": [40, 0],
	"red": [41, 64],
	"green": [42, 32],
	"yellow": [43, 96],
	"blue": [44, 16],
	"magenta": [45, 80],
	"cyan": [46, 48],
	"light-gray": [47, 112],
	"dark-gray": [100, 128],
	"light-red": [101, 192],
	"light-green": [102, 160],
	"light-yellow": [103, 224],
	"light-blue": [104, 144],
	"light-magenta": [105, 208],
	"light-cyan": [106, 176],
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
