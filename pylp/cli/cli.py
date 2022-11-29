"""

Start Pylp via the CLI.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

# Add parent folder into 'sys.path' if Pylp is not in Python 'Lib' folder.
import click
import os
from os import path

from pylp import __version__ as version
from pylp.lib import config
from pylp.cli.run import run

@click.command()
@click.version_option(version, prog_name='pylp')
@click.option('--pylpfile',  help="manually set path of pylpfile")
@click.option('--silent', is_flag=True,  help="disable all Pylp logging")
@click.option('--no-color', is_flag=True,  help="force Pylp to not display colors")
@click.option('--cwd',  help="manually set the CWD")
@click.argument('tasks', nargs=-1)
def launch_cli(pylpfile, silent, no_color, cwd, tasks):

    if not tasks:
        tasks=['default']
    else:
        tasks = list(tasks)

    print(f"pylpfile={pylpfile}, cwd={cwd}, silent={silent}, no_color={no_color}, tasks={tasks}")
    # return

    # Current working directory (CWD)
    if cwd:
        config.cwd = cwd
    else:
        config.cwd = os.getcwd()

    # Get the pylpfile location

    if not pylpfile:
        pylpfile = path.join(config.cwd, "pylpfile.py")
    elif not cwd:
        config.cwd = path.dirname(pylpfile)


    # Must the terminal have colors?
    config.color = not no_color

    # Must Pylp be silent (no logging)?
    config.silent = silent


    # Execute the pylpfile
    run(pylpfile, tasks)
