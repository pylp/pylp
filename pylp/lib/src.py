"""

Create a starting stream from local files.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import glob
import os
from . import config
from .file import File, FileReader
from .stream import Stream


# Parse a glob
def parse_glob(path, include, exclude):
	files = glob.glob(path, recursive=True)

	is_neg = path.startswith("!")
	array = exclude if is_neg else include

	for file in files:
		if file not in array:
			array.append(file)



# Remove excluded file from 'include' array
def apply_exclude(include, exclude):
	for file in exclude:
		if file in include:
			include.remove(file)



# Read some files and return a stream
def src(globs, **options):
	# Create an array of globs if only one string is given
	if isinstance(globs, str):
		globs = [ globs ]

	# List of files to include and exclude
	include = []
	exclude = []

	# Find files
	for path in globs:
		parse_glob(path, include, exclude)
	apply_exclude(include, exclude)

	# Create a stream
	stream = Stream()
	options["cwd"] = config.cwd

	# Create a File object for each file to include
	for file in include:
		file = File(file, **options)
		file.relpath = file.path
		stream.append_file(file)

	# No more files to add
	stream.end_of_stream()

	# Pipe a file reader and return the stream
	if options.get("read", True):
		return stream.pipe(FileReader())
	return stream
