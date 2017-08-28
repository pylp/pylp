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
def task(obj = None, deps = None):
	# The decorator is not used as a function
	if callable(obj):
		__task(obj.__name__, obj)
		return obj

	# The decorator is used as a function
	def __decorated(func):
		__task(obj if obj else obj.__name__, deps, func)
		return func
	return __decorated
