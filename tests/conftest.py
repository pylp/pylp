import os
import pylp

# https://stackoverflow.com/a/35394239/489239

def pytest_sessionstart(session):
    pylp.lib.config.cwd = os.getcwd()
