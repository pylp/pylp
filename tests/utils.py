"""

Some usefuls objects for doing unit tests.
Async test system is based on https://github.com/kwarunek/aiounittest

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import unittest
import asyncio
import inspect

from pylp.lib.runner import TaskEndTransformer
from pylp import Stream


# Create a function to wait for the end of the stream
def wait_processed(self):
	"""Wait until the stream have processed the files."""
	future = asyncio.Future()
	self.pipe(TaskEndTransformer(future))
	return future

# Set this function as a method of Stream
Stream.wait_processed = wait_processed

def async_test(func):
	"""Run an asynchrounous test."""

	loop = asyncio.get_event_loop()
	if loop.is_closed():
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)

	def test_func():
		future = asyncio.ensure_future(func(), loop=loop)
		loop.run_until_complete(future)

	test_func.__doc__ = func.__doc__
	return test_func


class AsyncTestCase(unittest.TestCase):
	"""A test case that supports asynchrounous methods."""

	def __getattribute__(self, name):
		func = super().__getattribute__(name)
		if name.startswith('test_') and inspect.iscoroutinefunction(func):
			return async_test(func)
		return func
