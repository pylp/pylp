"""

Write contents to local files.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .transformer import Transformer



# Return a transformer for writing files
def dest(path):
	return FileWriter(path)



# Get the writing path of a file
def get_path(dest, file):
	if callable(dest):
		return dest(file)

	if not os.path.isabs(dest):
		dest = os.path.join(file.cwd, dest)

	if file.base:
		relative = os.path.relpath(file.path, file.base)
	else:
		relative = os.path.basename(file.path)

	return os.path.join(dest, relative)


# Write a file
def write_file(path, contents):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "w") as file:
		file.write(contents)



# Transformer that save local files.
class FileWriter(Transformer):

	# Constructor
	def __init__(self, path):
		super().__init__()

		self.dest = path

		self.exe = ThreadPoolExecutor()
		self.loop = asyncio.get_event_loop()


	# Function called when a file need to be transformed
	async def transform(self, file):
		path = get_path(self.dest, file)
		await self.loop.run_in_executor(self.exe, write_file, path, file.contents)
