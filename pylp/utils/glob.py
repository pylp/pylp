"""

Some useful functions for using globs.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import glob
import re


# Separate include and exclude globs
def separate_globs(globs):
	exclude = []
	include = []

	for path in globs:
		if path.startswith("!"):
			exclude.append(path[1:])
		else:
			include.append(path)

	return (exclude, include)



# Parse a glob
def parse_glob(path, included):
	files = glob.glob(path, recursive=True)

	array = []

	for file in files:
		file = os.path.abspath(file)
		if file not in included:
			array.append(file)

	included += array
	return array



# Regex for finding the base
_pattern = re.compile("[a-z0-9_.-/~]+", re.I)

# Find the base of a glob
def find_base(path):
	result = _pattern.match(path)

	if result:
		base = result.group(0)
	else:
		base = "./"

	return os.path.dirname(os.path.abspath(base))
