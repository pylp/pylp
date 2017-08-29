"""

Setup Pylp.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

from setuptools import setup, find_packages
from pylp import __version__ as version


setup(
	name = "pylp",
	version = version,
	author = "Guillaume Gonnet",
	author_email = "gonnet.guillaume97@gmail.com",
	description = "A Python task runner inspired by gulp.js",
	long_description = open("README.rst").read(),
	license = "MIT",
	keywords = "pylp build task runner gulp",
	url = "https://github.com/pylp/pylp",
	packages = find_packages(),
	python_requires = ">=3.5",
	entry_points = {
		"console_scripts" : ["pylp = pylp.cli.cli:launch_cli",]
	},
	classifiers = [
		"Development Status :: 4 - Beta",
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
