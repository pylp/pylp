"""

Run a pylpfile.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

from typing import List
import runpy, os, sys
import traceback
import asyncio
import pylp
import pylp.cli.logger as logger
from pylp.utils.paths import make_readable_path


def run(path:str, tasks:List[str]):
    """Run a pylpfile.

    Args:
        path (str): path to pylpfile
        tasks (List[str]): names of tasks to be run
    """

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



async def wait_and_quit(loop):
    """Wait until all task are executed."""
    from pylp.lib.tasks import running
    if running:
        futures = list(map(lambda task_runner: task_runner.future, running))
        # await asyncio.wait(map(lambda task_runner: task_runner.future, running))
        await asyncio.wait(futures)
