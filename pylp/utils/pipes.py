"""

Some useful functions for using pipes.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""


# Pipe several transformers end to end
def pipes(stream, *transformers):
    for transformer in transformers:
        stream = stream.pipe(transformer)
    return stream
