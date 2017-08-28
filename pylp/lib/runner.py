"""

Some classes for running a task.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import asyncio
import inspect, time
import pylp
import pylp.cli.logger as logger
from pylp.lib.stream import Stream
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
		logger.log("Starting '", logger.cyan(self.name), "'...")


	# Log that this task is done
	def log_finished(self):
		delta = time.perf_counter() - self.start_time
		logger.log("Finished '", logger.cyan(self.name),
			"' after ", logger.magenta(time_to_text(delta)))



	# Call the function attached to the task
	def call_task_fn(self):
		if not self.fn:
			return self.log_finished()

		future = asyncio.Future()
		future.add_done_callback(lambda x: self.log_finished())

		if inspect.iscoroutinefunction(self.fn):
			f = asyncio.ensure_future(self.fn())
			f.add_done_callback(lambda x: self.bind_end(x.result(), future))
		else:
			self.bind_end(self.fn(), future)

		return future


	# Dind a 'TaskEndTransformer' to a stream
	def bind_end(self, stream, future):
		if not isinstance(stream, Stream):
			future.set_result(None)
		else:
			stream.pipe(TaskEndTransformer(future))



	# Start running dependencies
	async def start_deps(self, deps):
		# Get only new dependencies
		deps = list(filter(lambda dep: dep not in self.called, deps))
		self.called += deps

		# Start only existing dependencies
		runners = list(filter(lambda x: x and x.future, map(lambda dep: pylp.start(dep), deps)))
		if len(runners) != 0:
			await asyncio.wait(map(lambda runner: runner.future, runners))

		# Call the attached function 
		future = self.call_task_fn()
		if future:
			await future
