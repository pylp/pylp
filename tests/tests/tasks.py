"""

Test 'pylp.task' for defining a new task.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import pylp
from utils import AsyncTestCase


class TestTask(AsyncTestCase):
	"""Test 'pylp.task' for defining a new task."""

	def test_task_simple(self):
		"""It should define a task"""

		pylp.task('test', lambda: None)
		self.assertIn('test', pylp.lib.tasks.tasks)
