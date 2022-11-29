"""

Some classes for running a task.

Copyright (C) 2017 The Pylp Authors.
License GPL3

"""

import asyncio
import inspect
import time

import pylp
import pylp.cli.logger as logger
from pylp.lib.stream import Stream
from pylp.lib.transformer import Transformer
from pylp.utils.time import time_to_text


class TaskEndTransformer(Transformer):
    """Transformer that waits until a 'end-of-stream'."""

    def __init__(self, future):
        super().__init__()
        self.future = future

    async def flush(self):
        """Function called after when files are transformed."""
        self.future.set_result(None)




class TaskRunner():
    """This class executes a task."""

    @property
    def future(self):
        return self._future

    def __init__(self, name, fn, deps, called):
        self.name = name
        self.called = called if called else []
        self.fn = fn

        self.log_starting()

        if deps:
            self._future = self.start_deps(deps)
        else:
            self._future = self.call_task_fn()


    def log_starting(self):
        """Log that the task has started."""
        self.start_time = time.perf_counter()
        logger.log("Starting '", logger.cyan(self.name), "'...")


    def log_finished(self):
        """Log that this task is done."""
        delta = time.perf_counter() - self.start_time
        logger.log("Finished '", logger.cyan(self.name),
            "' after ", logger.magenta(time_to_text(delta)))


    def call_task_fn(self):
        """Call the function attached to the task."""
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


    def bind_end(self, stream, future):
        """Bind a 'TaskEndTransformer' to a stream."""
        if not isinstance(stream, Stream):
            future.set_result(None)
        else:
            stream.pipe(TaskEndTransformer(future))


    async def start_deps(self, deps):
        """Start running dependencies."""

        # Get only new dependencies
        deps = list(filter(lambda dep: dep not in self.called, deps))
        self.called += deps

        # Start only existing dependencies
        runners = list(filter(lambda x: x and x._future, map(lambda dep: pylp.start(dep), deps)))
        if len(runners) != 0:
            futures = list(map(lambda task_runner: task_runner.future, runners))
            await asyncio.wait(futures)

        # Call the attached function
        future = self.call_task_fn()
        if future:
            await future
