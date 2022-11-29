import os
import pylp
import pytest

import asyncio
from pylp.lib.runner import TaskEndTransformer

from pylp import Stream
from .utils import wait_processed

# Create a function to wait for the end of the stream
def wait_processed(self):
	"""Wait until the stream have processed the files."""
	future = asyncio.Future()
	self.pipe(TaskEndTransformer(future))
	return future

# https://stackoverflow.com/a/35394239/489239

def pytest_sessionstart(session):
    pylp.lib.config.cwd = os.getcwd()


@pytest.fixture(autouse=True)
def before__test():
    Stream.wait_processed = wait_processed
