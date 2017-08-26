"""

Pylp decorators.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import sys
from pylp.lib.tasks import task as __task


# Export this module as 'pylp.fn'
sys.modules['pylp.fn'] = sys.modules[__name__]


# Create a task
def task(name, deps = None):
	def __decorated(func):
		__task(name, deps, func)
		return func
	return __decorated
