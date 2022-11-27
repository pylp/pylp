import os
import pylp

# https://stackoverflow.com/questions/17801300/how-to-run-a-method-before-all-tests-in-all-classes

def pytest_sessionstart(session):
    pylp.lib.config.cwd = os.getcwd()
