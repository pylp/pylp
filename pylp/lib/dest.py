"""

Write contents to local files.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pylp.lib.transformer import Transformer



def dest(path, cwd = None):
	"""Return a transformer that writes contents to local files."""
	return FileWriter(path, cwd)



def get_path(dest, file, cwd = None):
	"""Get the writing path of a file."""
	if callable(dest):
		return dest(file)

	if not cwd:
		cwd = file.cwd
	if not os.path.isabs(dest):
		dest = os.path.join(cwd, dest)

	relative = os.path.relpath(file.path, file.base)
	return os.path.join(dest, relative)


def write_file(path, contents):
	"""Write contents to a local file."""
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "w") as file:
		file.write(contents)



class FileWriter(Transformer):
	"""Transformer that saves contents to local files."""

	def __init__(self, path, cwd = None):
		super().__init__()

		self.dest = path
		self.cwd = cwd

		self.exe = ThreadPoolExecutor()
		self.loop = asyncio.get_event_loop()


	async def transform(self, file):
		"""Function called when a file need to be transformed."""
		path = get_path(self.dest, file)
		await self.loop.run_in_executor(self.exe, write_file, path, file.contents)
		return file
