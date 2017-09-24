"""

Some useful functions for using pipes.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""


def pipes(stream, *transformers):
    """Pipe several transformers end to end."""
    for transformer in transformers:
        stream = stream.pipe(transformer)
    return stream
