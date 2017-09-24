"""

Create and run tasks.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import pylp.cli.logger as logger
from pylp.lib.runner import TaskRunner



# List of created tasks
tasks = {}

def task(name, deps = None, fn = None):
	"""Define a new task."""
	if callable(deps):
		fn = deps
		deps = None

	if not deps and not fn:
		logger.log(logger.red("The task '%s' is empty" % name))
	else:
		tasks[name] = [fn, deps]



# List of running task
running = []

def start(name, called = None):
	"""Start a task."""
	if name not in tasks:
		logger.log(logger.red("Task '%s' not in your pylpfile" % name))
	else:
		task = tasks[name]
		runner = TaskRunner(name, task[0], task[1], called)
		running.append(runner)
		return runner
