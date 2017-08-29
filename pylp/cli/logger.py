"""

Log some text into the terminal.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import time
import pylp.cli.colors as colors
import pylp.lib.config as config


# Color separators
# They can be used as follow: "~~color:text"
_color_sep = "~~"
_color_sep2 = ":"


# Create a function that set the foreground color
def _make_color_fn(color):
	def _color(text = ""):
		return (_color_sep + color + _color_sep2 + text +
			_color_sep + "default" + _color_sep2)
	return _color

# Create a function for each defined color
for _color in colors.foreground_colors.keys():
	globals()[_color] = _make_color_fn(_color)



# Log a text without adding the current time
def just_log(*texts, sep = ""):
	if config.silent:
		return

	text = _color_sep + "default" + _color_sep2 + sep.join(texts)
	array = text.split(_color_sep)

	for part in array:
		parts = part.split(_color_sep2, 1)
		if len(parts) != 2 or not parts[1]:
			continue

		if not config.color:
			print(parts[1], end='')
		else:
			colors.foreground(parts[0])
			print(parts[1], end='', flush=colors.is_win32)

	if config.color:
		colors.foreground("default")
	print()



# Get the current time (used as prefix in all logs)
def get_time():
	return ("[", darkgray(time.strftime("%H:%M:%S")), "] ")

# Log a text
def log(*texts, sep = ""):
	text = sep.join(texts)
	count = text.count("\n")
	just_log("\n" * count, *get_time(), text.replace("\n", ""), sep=sep)
