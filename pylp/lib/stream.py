"""

Stream with a piping system.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import asyncio


# An asynchronous stream containing a transformer
class Stream():

	# Constructor
	def __init__(self, files = None):
		# Files to transform and number of transformed
		self.files = files if files else []
		self.transformed = 0

		# Transformer, next and previous streams
		self.transformer = None
		self.next = None
		self.prev = None

		# Is the stream ended?
		self.ended = False

		# Events
		self.onpiped = asyncio.Future()



	# Append a new file in the stream
	def append_file(self, file):
		self.files.append(file)

		if self.transformer:
			future = asyncio.ensure_future(self.transformer.transform(file))
			future.add_done_callback(self.handle_transform)


	# Handle a 'transform' callback
	def handle_transform(self, task):
		self.transformed += 1
		file = task.result()

		if file:
			self.next.append_file(file)

		if self.ended and len(self.files) == self.transformed:
			future = asyncio.ensure_future(self.transformer.flush())
			future.add_done_callback(lambda x: self.next.end_of_stream())


	# Tell that no more files will be transformed
	def end_of_stream(self):
		self.ended = True

		if self.next and len(self.files) == self.transformed:
			future = asyncio.ensure_future(self.transformer.flush())
			future.add_done_callback(lambda x: self.next.end_of_stream())



	# Pipe this stream to another
	def pipe(self, transformer):
		if self.next:
			return

		stream = Stream()
		self.next = stream
		stream.prev = self

		self.transformer = transformer
		transformer.stream = self
		transformer.piped()

		for file in self.files:
			future = asyncio.ensure_future(self.transformer.transform(file))
			future.add_done_callback(self.handle_transform)	

		self.onpiped.set_result(None)
		return stream
