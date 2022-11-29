import os
import pylp
import pytest

import asyncio
from pylp.lib.runner import TaskEndTransformer

from pylp import Stream
from .utils import wait_processed

# Create a function to wait for the end of the stream
def wait_processed(self):
	"""Wait until the stream have processed the files."""
	future = asyncio.Future()
	self.pipe(TaskEndTransformer(future))
	return future

# https://stackoverflow.com/a/35394239/489239

def pytest_sessionstart(session):
    pylp.lib.config.cwd = os.getcwd()


@pytest.fixture(autouse=True)
def before__test():
    Stream.wait_processed = wait_processed

"""

Test 'pylp.src' for creating an input stream.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import pytest
from os.path import abspath
import pylp

# https://github.com/gulpjs/gulp/blob/master/test/src.js

@pytest.mark.asyncio
class TestInputStream:
	"""Test 'pylp.src' for creating an input stream"""

	async def test_src_simple(self):
		"""It should return a stream"""

		stream = pylp.src("./tests/unit/fixtures/file.txt")
		assert isinstance(stream, pylp.Stream)


	async def test_src_glob(self):
		"""It should return a stream from a glob, matching one file"""

		stream = pylp.src("./tests/unit/fixtures/*.txt")
		await stream.wait_processed()

		assert len(stream.files) == 1
		file = stream.files[0]

		assert isinstance(file, pylp.File)
		assert file.path == abspath("./tests/unit/fixtures/file.txt")
		assert file.contents == "This is a test file."


	async def test_src_multiple_glob(self):
		"""It should return a stream from multiple globs"""

		files = [
			"./tests/unit/fixtures/some-files/file1.ext",
			"./tests/unit/fixtures/some-files/file2.ext"
		]

		stream = pylp.src(files)
		await stream.wait_processed()

		assert len(stream.files) == len(files)
		stream.files.sort(key=lambda f: f.order)

		for i, path, file in zip(range(len(files)), files, stream.files):
			assert isinstance(file, pylp.File)
			assert file.path == abspath(path)
			assert file.order == i+1


	async def test_src_multiple_glob_negation(self):
		"""It should return a stream from multiple globs, with negation"""

		stream = pylp.src([
			"./tests/unit/fixtures/some-files/*.ext",
			"!./tests/unit/fixtures/some-files/file2.ext"
		])

		await stream.wait_processed()

		assert len(stream.files) == 1

		file = stream.files[0]

		assert isinstance(file, pylp.File)
		assert file.path == abspath("./tests/unit/fixtures/some-files/file1.ext")


	async def test_src_read_false(self):
		"""It should return a stream, without reading contents"""

		stream = pylp.src("./tests/unit/fixtures/*.txt", read=False)
		await stream.wait_processed()

		assert len(stream.files) == 1

		file = stream.files[0]

		assert isinstance(file, pylp.File)
		assert file.path == abspath("./tests/unit/fixtures/file.txt")
		assert file.contents == ""


	async def test_src_deep_glob(self):
		"""It should return a stream from a deep glob"""

		files = [
			("./tests/unit/fixtures/file.txt", "This is a test file."),
			("./tests/unit/fixtures/some-files/file3.txt", "This is another test file.")
		]

		stream = pylp.src("./tests/unit/fixtures/**/*.txt")
		await stream.wait_processed()

		assert len(stream.files) == len(files)

		stream.files.sort(key=lambda f: f.path)
		files.sort(key=lambda x: x[0])

		for (path, contents), file in zip(files, stream.files):
			assert isinstance(file, pylp.File)
			assert file.path == abspath(path)
			assert file.contents == contents


	async def test_src_same_file(self):
		"""It should return a stream, with no duplicates"""

		files = [
			("./tests/unit/fixtures/file.txt", "This is a test file."),
			("./tests/unit/fixtures/some-files/file3.txt", "This is another test file.")
		]

		stream = pylp.src(["./tests/unit/fixtures/**/*.txt", "./tests/unit/fixtures/*.txt"])
		await stream.wait_processed()

		assert len(stream.files) == len(files)

		for (path, contents), file in zip(files, stream.files):
			assert isinstance(file, pylp.File)
			assert file.path == abspath(path)
			assert file.contents == contents

"""

Test 'pylp.task' for defining a new task.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import pylp


class TestTask:
	"""Test 'pylp.task' for defining a new task."""

	def test_task_simple(self):
		"""It should define a task"""

		pylp.task('test', lambda: None)
		assert 'test' in pylp.lib.tasks.task_registry

"""

Test 'pylp.dest' for writing contents to local files.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os, os.path as path
import pytest
import shutil
import pylp

from pylp.lib.dest import FileWriter


# https://github.com/gulpjs/gulp/blob/master/test/dest.js

@pytest.mark.asyncio
class TestDestTransformer:
    """Test 'pylp.dest' for writing contents to local files."""

    def setup_method(self, test_method):
        self.out_folder = "tests/unit/out-fixtures/"

        shutil.rmtree(self.out_folder, ignore_errors=True)
        os.mkdir(self.out_folder)

    def teardown_method(self):
        shutil.rmtree(self.out_folder, ignore_errors=True)

    async def test_dest_simple(self):
        """It should return a writing transformer"""

        transformer = pylp.dest("tests/unit/fixtures/")
        assert isinstance(transformer, FileWriter)


    async def test_dest_copy(self):
        """It should copy a file into the destination folder"""

        stream = pylp.src("tests/unit/fixtures/*.txt").pipe(pylp.dest(self.out_folder))
        await stream.wait_processed()

        filename = path.join(self.out_folder, "file.txt")

        assert path.isfile(filename)

        with open(filename, "r") as file:
            assert file.read() == "This is a test file."


    async def test_dest_copy_base(self):
        """It should copy a file into the destination folder, keeping the base folder"""

        stream = pylp.src("tests/unit/fixtures/**/*.ext2").pipe(pylp.dest(self.out_folder))
        await stream.wait_processed()

        filename = path.join(self.out_folder, "other-files/a-file.ext2")
        assert path.isfile(filename)

        with open(filename, "r") as file:
            assert file.read(), "A file in a folder."

"""

Test transformers contained in streams.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import pytest
import pylp


class UpperTransformer(pylp.Transformer):
	"""A transformer that capitalizes contents."""

	async def transform(self, file):
		"""Function called when a file need to be transformed."""
		file.contents = file.contents.upper()
		return file


class ReverseTransformer(pylp.Transformer):
	"""A transformer that reverses contents."""

	async def transform(self, file):
		"""Function called when a file need to be transformed."""
		file.contents = file.contents[::-1]
		return file



class RecorderTransformer(pylp.Transformer):
	"""A transformer that record files passed inside."""

	def __init__(self):
		self.files = []

	async def transform(self, file):
		"""Function called when a file need to be transformed."""
		self.files.append(file.clone())
		return file


@pytest.mark.asyncio
class TestTransformer:
	"""Test transformers contained in streams."""

	async def test_transformer_upper(self):
		"""It should capitalize contents."""

		stream = pylp.src("./tests/unit/fixtures/file.txt").pipe(UpperTransformer())
		await stream.wait_processed()

		assert len(stream.files) == 1
		file = stream.files[0]

		assert  isinstance(file, pylp.File)
		assert file.contents == "THIS IS A TEST FILE."


	async def test_transformer_multiple(self):
		"""It should run multiple transformers."""

		recorder = RecorderTransformer()
		stream = pylp.pipes(
			pylp.src("./tests/unit/fixtures/file.txt"),
			UpperTransformer(),
			recorder,
			ReverseTransformer()
		)

		await stream.wait_processed()

		assert len(stream.files) == 1
		assert len(recorder.files) == 1

		assert recorder.files[0].contents == "THIS IS A TEST FILE."
		assert stream.files[0].contents == ".ELIF TSET A SI SIHT"

"""

Some usefuls objects for doing unit tests.
Async test system is based on https://github.com/kwarunek/aiounittest

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import asyncio

from pylp.lib.runner import TaskEndTransformer
from pylp import Stream


# Create a function to wait for the end of the stream
def wait_processed(self):
	"""Wait until the stream have processed the files."""
	future = asyncio.Future()
	self.pipe(TaskEndTransformer(future))
	return future

