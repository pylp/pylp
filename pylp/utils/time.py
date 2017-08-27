"""

Some useful functions for manipulating time.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""


# Get a representative text of a time (in s)
def time_to_text(time):
    if time < 0.001:
        return str(round(time * 1000000)) + " µs"
    elif time < 1:
        return str(round(time * 1000)) + " ms"
    elif time < 60:
        return str(round(time, 1)) + " s"
    else:
        return str(round(time / 60, 1)) + " min"