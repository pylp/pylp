"""

A class for transforming contents.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import asyncio


class Transformer():
    """This class transform contents."""

    def __init__(self):
        self.stream = None


    def append(self, file):
        """Append a new file in the stream."""
        self.stream.next.append_file(file)


    def piped(self):
        """Function called when the transformer is piped to a stream."""
        pass

    async def transform(self, file):
        """Function called when a file need to be transformed."""
        pass

    async def flush(self):
        """Function called when all files have been transformed."""
        pass
