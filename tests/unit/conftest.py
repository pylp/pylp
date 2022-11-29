import os
import pylp
import pytest

from pylp import Stream
from .utils import wait_processed
import pylp.lib.config as config


@pytest.fixture(autouse=True)
def before_test():
    config.cwd = os.getcwd()
    Stream.wait_processed = wait_processed
