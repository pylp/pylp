import shutil
from pylp.cli.cli import launch_cli

def test_cli_version(cli_runner):
    result = cli_runner.invoke(launch_cli, args=["--version"])
    assert result.output == 'pylp, version 0.2.10\n'


def xtest_cli(cli_runner):
    shutil.rmtree('./tests/integration/.build', ignore_errors=True)
    result = cli_runner.invoke(launch_cli, args=["--pylpfile=./tests/integration/pylpfile.py"])
    assert str(result) == '<Result okay>'

