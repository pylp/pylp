"""

Some useful functions.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""


# Pipe several transformers end to end
def pipes(stream, *transformers):
    for transformer in transformers:
        stream = stream.pipe(transformer)
    return stream


# Get a representative text of a time (in s)
def time_to_text(time):
    if time < 1:
        return str(round(time * 1000)) + " ms"
    else:
        return str(round(time, 1)) + " s"
