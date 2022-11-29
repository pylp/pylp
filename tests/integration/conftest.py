import shutil
import pytest


@pytest.fixture(autouse=True)
def before_test():
    shutil.rmtree('./tests/integration/.build', ignore_errors=True)
