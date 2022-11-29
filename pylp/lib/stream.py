"""

Asynchronous stream with a piping system.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import asyncio


class Stream():
    """An asynchronous stream containing a transformer with a piping system."""

    def __init__(self, files = None):
        # Files to transform and number of transformed
        self.files = files if files else []
        self.transformed = 0

        # Transformer, next and previous streams
        self.transformer = None
        self.next = None
        self.prev = None

        # Is the stream ended?
        self.ended = False

        # Events
        self.onpiped = asyncio.Future()


    def append_file(self, file):
        """Append a new file in the stream."""
        self.files.append(file)

        if self.transformer:
            future = asyncio.ensure_future(self.transformer.transform(file))
            future.add_done_callback(self.handle_transform)


    def flush_if_ended(self):
        """Call 'flush' function if all files have been transformed."""
        if self.ended and self.next and len(self.files) == self.transformed:
            future = asyncio.ensure_future(self.transformer.flush())
            future.add_done_callback(lambda x: self.next.end_of_stream())


    def handle_transform(self, task):
        """Handle a 'transform' callback."""
        self.transformed += 1

        file = task.result()
        if file:
            self.next.append_file(file)

        self.flush_if_ended()


    def end_of_stream(self):
        """Tell that no more files will be transformed."""
        self.ended = True
        self.flush_if_ended()


    def pipe(self, transformer):
        """Pipe this stream to another."""
        if self.next:
            return

        stream = Stream()
        self.next = stream
        stream.prev = self

        self.transformer = transformer
        transformer.stream = self
        transformer.piped()

        for file in self.files:
            future = asyncio.ensure_future(self.transformer.transform(file))
            future.add_done_callback(self.handle_transform)

        self.onpiped.set_result(None)
        self.flush_if_ended()

        return stream
