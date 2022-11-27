"""

Test 'pylp.src' for creating an input stream.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import pytest
from os.path import abspath
import pylp
from tests.utils import AsyncTestCase


@pytest.mark.asyncio
class TestInputStream:
	"""Test 'pylp.src' for creating an input stream"""

	async def test_src_simple(self):
		"""It should return a stream"""

		stream = pylp.src("./tests/fixtures/file.txt")
		assert isinstance(stream, pylp.Stream)


	async def test_src_glob(self):
		"""It should return a stream from a glob, matching one file"""

		stream = pylp.src("./tests/fixtures/*.txt")
		await stream.wait_processed()

		assert len(stream.files) == 1
		file = stream.files[0]

		assert isinstance(file, pylp.File)
		assert file.path == abspath("./tests/fixtures/file.txt")
		assert file.contents == "This is a test file."


	async def test_src_multiple_glob(self):
		"""It should return a stream from multiple globs"""

		files = [
			"./tests/fixtures/some-files/file1.ext",
			"./tests/fixtures/some-files/file2.ext"
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
			"./tests/fixtures/some-files/*.ext",
			"!./tests/fixtures/some-files/file2.ext"
		])

		await stream.wait_processed()

		assert len(stream.files) == 1

		file = stream.files[0]

		assert isinstance(file, pylp.File)
		assert file.path == abspath("./tests/fixtures/some-files/file1.ext")


	async def test_src_read_false(self):
		"""It should return a stream, without reading contents"""

		stream = pylp.src("./tests/fixtures/*.txt", read=False)
		await stream.wait_processed()

		assert len(stream.files) == 1

		file = stream.files[0]

		assert isinstance(file, pylp.File)
		assert file.path == abspath("./tests/fixtures/file.txt")
		assert file.contents == ""


	async def test_src_deep_glob(self):
		"""It should return a stream from a deep glob"""

		files = [
			("./tests/fixtures/file.txt", "This is a test file."),
			("./tests/fixtures/some-files/file3.txt", "This is another test file.")
		]

		stream = pylp.src("./tests/fixtures/**/*.txt")
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
			("./tests/fixtures/file.txt", "This is a test file."),
			("./tests/fixtures/some-files/file3.txt", "This is another test file.")
		]

		stream = pylp.src(["./tests/fixtures/**/*.txt", "./tests/fixtures/*.txt"])
		await stream.wait_processed()

		assert len(stream.files) == len(files)

		for (path, contents), file in zip(files, stream.files):
			assert isinstance(file, pylp.File)
			assert file.path == abspath(path)
			assert file.contents == contents
