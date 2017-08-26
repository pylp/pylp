"""

Store the content of a file.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pylp.lib.transformer import Transformer


# The file class
class File():

	# Constructor
	def __init__(self, path, **options):
		# Path of the file
		self.path = os.path.abspath(path)
		self.relpath = None
		self.cwd = options.get('cwd')
		self.relative = os.path.relpath(path, self.cwd)

		# Contents of the file
		self.contents = options.get("contents", "")

		# Options
		self.base = options.get("base")




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
