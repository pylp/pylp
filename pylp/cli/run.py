"""

Run a pylpfile.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import runpy, os, sys
import traceback
import asyncio
import pylp, pylp.cli.logger as logger


# Run a pylpfile
def run(path, tasks):
	# Test if the pylpfile exists
	is_file = os.path.isfile(path)

	if not os.path.isfile(path):
		logger.error("Can't read pylpfile ")
	else:
		logger.log("Using pylpfile ")

	logger.info(path)
	logger.reset()

	if not is_file:
		return


	# Run the pylpfile
	try:
		runpy.run_path(path, None, "pylpfile")
	except Exception as e:
		traceback.print_exc(file=sys.stdout)
		logger.reset()
		logger.error("An error has occurred during the execution of the pylpfile")
		logger.reset()
		return


	# Start the tasks
	for name in tasks:
		pylp.start(name)

	# Wait until all task are executed
	loop = asyncio.get_event_loop()
	loop.run_until_complete(wait_and_quit(loop))



# Wait until all task are executed 
async def wait_and_quit(loop):
	from pylp.lib.tasks import running
	await asyncio.wait(map(lambda runner: runner.future, running))
