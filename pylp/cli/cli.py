"""

Start Pylp via the CLI.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

# Add parent folder into 'sys.path' if Pylp is not in Python 'Lib' folder.
import os, sys
import os.path as path

relpath = path.dirname(path.realpath(__file__))
parent = path.normpath(path.realpath(path.join(relpath, "../..")))

if not parent.lower().endswith(path.normpath("lib/site-packages")):
	sys.path.insert(0, os.path.abspath(parent))


# We can import now all Pylp files
import argparse
from pylp import __version__ as version
import pylp.lib.config as config
from pylp.cli.run import run



# Launch the CLI
def launch_cli():
	# Create the CLI argument parser
	parser = argparse.ArgumentParser(
		prog="pylp",
		description="Call some tasks defined in your pylpfile."
	)


	# Version of Pylp
	parser.add_argument("-v", "--version",
		action="version",
		version="Pylp %s" % version,
		help="get the Pylp version and exit"
	)

	# Set the pylpfile location
	parser.add_argument('--pylpfile',
		nargs=1,
		help="manually set path of pylpfile",
		metavar="<path>"
	)

	# Set the pylpfile location
	parser.add_argument('--cwd',
		nargs=1,
		help="manually set the CWD",
		metavar="<dir path>"
	)

	# List of tasks to execute
	parser.add_argument('tasks',
		nargs="*",
		default=["default"],
		help="tasks to execute (if none, execute the 'default' task)",
		metavar="<task>"
	)


	# Parse the CLI arguments
	args = parser.parse_args()


	# Current working directory (CWD)
	if args.cwd:
		config.cwd = args.cwd[0]
	else:
		config.cwd = os.getcwd()

	# Get the pylpfile location
	if args.pylpfile:
		pylpfile = args.pylpfile[0]

	if not args.pylpfile:
		pylpfile = path.join(config.cwd, "pylpfile.py")
	elif not args.cwd:
		config.cwd = path.dirname(pylpfile)


	# Execute the pylpfile
	run(pylpfile, args.tasks)



# Launch the CLI if this file is executed directly
if __name__ == "__main__":
    launch_cli()
