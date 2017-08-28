"""

Some classes for running a task.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import asyncio
import time
import pylp
import pylp.cli.logger as logger
from pylp.lib.transformer import Transformer
from pylp.utils.time import time_to_text



# Wait until a 'end-of-stream'
class TaskEndTransformer(Transformer):

	# Constructor
	def __init__(self, future):
		super().__init__()
		self.future = future

	# Function called after when files are transformed.
	async def flush(self):
		self.future.set_result(None)




# Execute a task
class TaskRunner():

	# Constructor
	def __init__(self, name, fn, deps, called):
		self.name = name
		self.called = called if called else []
		self.fn = fn

		self.log_starting()	

		if deps:
			self.future = self.start_deps(deps)
		else:
			self.future = self.call_task_fn()


	# Log that the task has started
	def log_starting(self):
		self.start_time = time.perf_counter()

		logger.log("Starting '")
		logger.name(self.name)
		logger.log("'...")
		logger.reset()


	# Log that this task is done
	def log_finished(self):
		delta = time.perf_counter() - self.start_time

		logger.log("Finished '")
		logger.name(self.name)
		logger.log("' after ")
		logger.info(time_to_text(delta))
		logger.reset()


	# Call the function attached to the task
	def call_task_fn(self):
		if not self.fn:
			self.log_finished()
		else:
			future = asyncio.Future()
			future.add_done_callback(lambda x: self.log_finished())
			self.fn().pipe(TaskEndTransformer(future))
			return future


	# Start running dependencies
	async def start_deps(self, deps):
		# Get only new dependencies
		deps = list(filter(lambda dep: dep not in self.called, deps))
		self.called += deps

		# Start only existing dependencies
		runners = list(filter(lambda x: x, map(lambda dep: pylp.start(dep), deps)))
		if len(runners) != 0:
			await asyncio.wait(map(lambda runner: runner.future, runners))

		# Call the attached function 
		future = self.call_task_fn()
		if future:
			await future
