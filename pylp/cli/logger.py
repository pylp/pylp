"""

Log some text into the terminal.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import time
import pylp.cli.colors as colors


# Print a message with a color
def cprint(text):
	print(text, end='', flush=colors.is_win32)


# Do we have reset the line?
have_reset = True

# Reset the color and add a new line
def reset(newLine = True):
	global have_reset
	colors.foreground("default")
	have_reset = True
	if newLine:
		print()


# Log the current time (used as prefix in all logs)
def log_time():
	global have_reset
	if have_reset:
		colors.foreground("default")
		cprint("[")
		colors.foreground("dark-gray")
		cprint(time.strftime("%H:%M:%S"))
		colors.foreground("default")
		cprint("] ")
		have_reset = False


# Log a normal text
def log(text):
	log_time()
	colors.foreground("default")
	cprint(text)

# Log an information
def info(text):
	log_time()
	colors.foreground("magenta")
	cprint(text)

# Log an name
def name(text, newLine = False):
	log_time()
	colors.foreground("cyan")
	cprint(text)

# Log an error
def error(text, newLine = False):
	log_time()
	colors.foreground("red")
	cprint(text)
