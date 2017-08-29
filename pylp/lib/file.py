"""

Store the content of a file.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pylp.lib.transformer import Transformer


# Infinity value for file order
_inf = float('Inf')



# The file class
class File():

	# Constructor
	def __init__(self, path, **options):
		# Options
		self.order = _inf
		self.base = options.get("base", os.path.dirname(path))

		# Path of the file
		self.cwd = options.get("cwd")
		self.set_path(path)
		self.relpath = None

		# Contents of the file
		self.contents = options.get("contents", "")


	# Set the path of the file
	def set_path(self, path):
		if os.path.isabs(path):
			path = os.path.normpath(os.path.join(self.cwd, path))

		self.path = path
		self.relative = os.path.relpath(self.path, self.base)


	# Clone the file
	def clone(path = None, *, with_contents = True, **options):
		file = File(path if path else self.path, cwd=options.get("cwd", self.cwd))
		file.base = options.get("base", self.base)

		if with_contents:
			file.contents = options.get("contents", self.contents)

		return file




# Read a local file
class FileReader(Transformer):

	# Constructor
	def __init__(self):
		super().__init__()

		self.exe = ThreadPoolExecutor()
		self.loop = asyncio.get_event_loop()


	# Read a file
	def read_file(self, path):
		with open(path, "r") as file:
			return file.read()


	# Function called when a file need to be transformed
	async def transform(self, file):
		file.contents = await self.loop.run_in_executor(self.exe, self.read_file, file.path)
		return file
