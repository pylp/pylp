"""

Create a stream from local files.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import pylp.lib.config as config
from pylp.utils.glob import separate_globs, parse_glob, find_base
from pylp.lib.file import File, FileReader
from pylp.lib.stream import Stream


def find_files(globs):
	"""Find files to include."""

	last_cwd = os.getcwd()
	os.chdir(config.cwd)

	gex, gin = separate_globs(globs)

	# Find excluded files
	exclude = []
	for glob in gex:
		parse_glob(glob, exclude)

	files = []
	include = []
	order = 0

	# Find included files and removed excluded files
	for glob in gin:
		order += 1
		array = parse_glob(glob, include)
		base = find_base(glob)

		for file in array:
			if file not in exclude:
				files.append((order, base, file))

	os.chdir(last_cwd)
	return files



def src(globs, **options):
	"""Read some files and return a stream."""

	# Create an array of globs if only one string is given
	if isinstance(globs, str):
		globs = [ globs ]

	# Find files
	files = find_files(globs)

	# Create a stream
	stream = Stream()

	# Options
	options["cwd"] = config.cwd

	if "base" in options:
		options["base"] = os.path.abspath(options["base"])

	# Create a File object for each file to include
	for infile in files:
		file = File(infile[2], **options)
		file.relpath = file.path
		file.order = infile[0]
		file.base = options.get("base", infile[1])
		stream.append_file(file)

	# No more files to add
	stream.end_of_stream()

	# Pipe a file reader and return the stream
	if options.get("read", True):
		return stream.pipe(FileReader())
	return stream



def readnow():
	"""Return a transformer that reads the files now (to be used with 'read=False')."""
	return FileReader()
