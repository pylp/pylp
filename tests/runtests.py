"""

Run all unit tests.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import unittest


# Add parent folder into 'sys.path' for loading Pylp.
import os, sys
import os.path as path

relpath = path.dirname(path.realpath(__file__))
parent = path.normpath(path.realpath(path.join(relpath, "..")))
sys.path.insert(0, parent)


# Setup Pylp
import pylp
pylp.lib.config.cwd = os.getcwd()


# Import the tests
from tests.src import TestInputStream
from tests.dest import TestDestTransformer
from tests.tasks import TestTask
from tests.transformer import TestTransformer


if __name__ == '__main__':
	unittest.main()
