"""

Run a pylpfile.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import runpy, os, sys
import traceback
import asyncio
import pylp
import pylp.cli.logger as logger
from pylp.utils.paths import make_readable_path


# Run a pylpfile
def run(path, tasks):
	# Test if the pylpfile exists
	readable_path = make_readable_path(path)
	if not os.path.isfile(path):
		logger.log(logger.red("Can't read pylpfile "), logger.magenta(readable_path))
		sys.exit(-1)
	else:
		logger.log("Using pylpfile ", logger.magenta(readable_path))


	# Run the pylpfile
	try:
		runpy.run_path(path, None, "pylpfile")
	except Exception as e:
		traceback.print_exc(file=sys.stdout)
		logger.log(logger.red("\nAn error has occurred during the execution of the pylpfile"))
		sys.exit(-1)


	# Start the tasks
	for name in tasks:
		pylp.start(name)

	# Wait until all task are executed
	loop = asyncio.get_event_loop()
	loop.run_until_complete(wait_and_quit(loop))



# Wait until all task are executed 
async def wait_and_quit(loop):
	from pylp.lib.tasks import running
	if running:
		await asyncio.wait(map(lambda runner: runner.future, running))
