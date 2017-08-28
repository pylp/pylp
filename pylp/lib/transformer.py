"""

Transform a stream to another.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import asyncio


# The transformr class
class Transformer():

	# Constructor
	def __init__(self):
		self.stream = None


	# Append a new file in the stream
	def append(self, file):
		self.stream.next.append_file(file)


	# Function called when the transformer is piped to a stream
	def piped():
		pass

	# Function called when a file need to be transformed
	async def transform(self, file):
		pass

	# Function called when all files are transformed
	async def flush(self):
		pass
