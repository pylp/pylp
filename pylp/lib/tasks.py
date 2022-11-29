"""

Create and run tasks.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

from typing import List
from collections import namedtuple
import pylp.cli.logger as logger
from pylp.lib.runner import TaskRunner


# List of tasks defined in pylpfile.py

task_registry = {}

def task(name, deps = None, fn = None):
    """Define a new task."""

    logger.log("Register task ", name)

    if callable(deps):
        fn = deps
        deps = None

    if not deps and not fn:
        logger.log(logger.red("The task '%s' is empty" % name))
    else:
        Task = namedtuple("Task", "fn deps")
        task_registry[name] = Task(fn, deps)



# List of running task
running: List[TaskRunner] = []

def start(name, called = None):
    """Start a task."""
    if name not in task_registry:
        logger.log(logger.red("Task '%s' not in your pylpfile" % name))
    else:
        task = task_registry[name]
        runner = TaskRunner(name, task.fn, task.deps, called)
        running.append(runner)
        return runner
