"""

Some useful functions for using paths.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os.path


def make_readable_path(path):
    """Make a path more "readable"""
    home = os.path.expanduser("~")
    if path.startswith(home):
        path = "~" + path[len(home):]

    return path
