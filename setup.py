"""

Setup Pylp.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os
from setuptools import setup
from . import __version__ as version


# Read a file
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Setup Pylp
setup(
	name = "pylp",
	version = version,
	author = "Guillaume Gonnet",
	description = ("A Python task runner inspired by gulp.js"),
	license = "MIT",
	keywords = "pylp build task runner gulp",
	url = "https://github.com/pylp/pylp",
	packages=['pylp'],
	long_description = read('README.md'),
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Topic :: Utilities",		
		"Topic :: Software Development :: Build Tools",
		"Framework :: AsyncIO",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.5",
		"Intended Audience :: Developers",
		"Natural Language :: English",
		"License :: OSI Approved :: MIT License",
	],
)