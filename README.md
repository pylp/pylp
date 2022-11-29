# Pylp

[![Build Status][build_status_badge]][build_status_link]
[![PyPI](https://img.shields.io/pypi/v/pylp.svg)](https://pypi.org/project/pylp)
[![PyPI](https://img.shields.io/pypi/format/pylp.svg)]()
[![PyPI](https://img.shields.io/pypi/pyversions/pylp.svg)]()

## What is pylp?

Pylp is a task runner for Python3 that lets you automate tasks.
It's inspired by [gulp.js](https://gulpjs.com).

Pylp use a syntax similar to Gulp, making this task runner easy to learn and simple to use.
Task process is completely asynchronous thanks to `asyncio` module, which provides a fast execution.


## Documentation

Check out the [documentation](/docs/README.md) for a Getting started guide, API docs or
making a plugin.


## Sample `pylpfile.py`

This file is an example of what you can do with Pylp.

```python
import pylp
from pylpconcat import concat

# Concat all js files from 'src' folder
pylp.task('js', lambda:
    pylp.src('src/**/*.js')
      .pipe(concat('all.min.js'))
      .pipe(pylp.dest('build/js'))
)

# The default task (called when you run 'pylp' from cli)
pylp.task('default', ['js'])
```

## Running Tests

  python pylp.py --pylpfile tests/integration/pylpfile.py

  pytest tests/unit

  pytest tests/integration

  pytest


[build_status_badge]: https://github.com/stevej2608/pylp/actions/workflows/test.yml/badge.svg
[build_status_link]: https://github.com/stevej2608/pylp/actions/workflows/test.yml
