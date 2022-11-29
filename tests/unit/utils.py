"""

Some usefuls objects for doing unit tests.
Async test system is based on https://github.com/kwarunek/aiounittest

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import asyncio

from pylp.lib.runner import TaskEndTransformer
from pylp import Stream


# Create a function to wait for the end of the stream
def wait_processed(self):
	"""Wait until the stream have processed the files."""
	future = asyncio.Future()
	self.pipe(TaskEndTransformer(future))
	return future
