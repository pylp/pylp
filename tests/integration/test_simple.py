from os import path
from pylp.cli.cli import launch_cli


def line_count(filename):
    lines = 0
    for line in open(filename):
        lines += 1
    return lines

def test_cli_version(cli_runner):
    result = cli_runner.invoke(launch_cli, args=["--version"])
    assert result.output == 'pylp, version 0.2.10\n'

def test_cli(cli_runner):
    OUT_FILE = './tests/integration/.build/all.py'
    result = cli_runner.invoke(launch_cli, args=["--pylpfile=./tests/integration/pylpfile.py"])

    assert str(result) == '<Result okay>'

    assert path.isfile(OUT_FILE)
    assert line_count(OUT_FILE) == 336


def test_cli_cwd(cli_runner):

    # Same test as above but use --cwd switch

    OUT_FILE = './tests/integration/.build/all.py'
    result = cli_runner.invoke(launch_cli, args=["--cwd=./tests/integration"])

    assert str(result) == '<Result okay>'
    assert path.isfile(OUT_FILE)
    assert line_count(OUT_FILE) == 336
