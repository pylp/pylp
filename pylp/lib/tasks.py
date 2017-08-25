"""

Create and run tasks.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import pylp.cli.logger as logger
from .runner import TaskRunner



# List of created tasks
tasks = {}

# Define a new task.
def task(name, deps = None, fn = None):
	if callable(deps):
		fn = deps
		deps = None

	if not deps and not fn:
		logger.error("The task '%s' is empty" % name)
		logger.reset()
	else:
		tasks[name] = [fn, deps]



# List of running task
running = []

# Start a task
def start(name, called = None):
	if name not in tasks:
		logger.error("Task '%s' not in your pylpfile" % name)
		logger.reset()
	else:
		task = tasks[name]
		runner = TaskRunner(name, task[0], task[1], called)
		running.append(runner)
		return runner
