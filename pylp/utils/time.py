"""

Some useful functions for manipulating time.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""


def time_to_text(time):
    """Get a representative text of a time (in s)."""

    if time < 0.001:
        return str(round(time * 1000000)) + " µs"
    if time < 1:
        return str(round(time * 1000)) + " ms"
    if time < 60:
        return str(round(time, 1)) + " s"

    return str(round(time / 60, 1)) + " min"
