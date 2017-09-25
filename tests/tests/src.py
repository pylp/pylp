"""

Test 'pylp.src' for creating an input stream.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

from os.path import abspath
import pylp
from utils import AsyncTestCase


class TestInputStream(AsyncTestCase):
	"""Test 'pylp.src' for creating an input stream"""

	def test_src_simple(self):
		"""It should return a stream"""

		stream = pylp.src("./fixtures/file.txt")
		self.assertIsInstance(stream, pylp.Stream)


	async def test_src_glob(self):
		"""It should return a stream from a glob, matching one file"""

		stream = pylp.src("./fixtures/*.txt")
		await stream.wait_processed()

		self.assertEqual(len(stream.files), 1)
		file = stream.files[0]

		self.assertIsInstance(file, pylp.File)
		self.assertEqual(file.path, abspath("./fixtures/file.txt"))
		self.assertEqual(file.contents, "This is a test file.")


	async def test_src_multiple_glob(self):
		"""It should return a stream from multiple globs"""
		
		files = [
			"fixtures/some-files/file1.ext",
			"fixtures/some-files/file2.ext"
		]

		stream = pylp.src(files)
		await stream.wait_processed()

		self.assertEqual(len(stream.files), len(files))
		stream.files.sort(key=lambda f: f.order)

		for i, path, file in zip(range(len(files)), files, stream.files):
			self.assertIsInstance(file, pylp.File)
			self.assertEqual(file.path, abspath(path))
			self.assertEqual(file.order, i+1)


	async def test_src_multiple_glob_negation(self):
		"""It should return a stream from multiple globs, with negation"""

		stream = pylp.src([
			"fixtures/some-files/*.ext",
			"!fixtures/some-files/file2.ext"
		])
		await stream.wait_processed()

		self.assertEqual(len(stream.files), 1)
		file = stream.files[0]

		self.assertIsInstance(file, pylp.File)
		self.assertEqual(file.path, abspath("fixtures/some-files/file1.ext"))


	async def test_src_read_false(self):
		"""It should return a stream, without reading contents"""

		stream = pylp.src("fixtures/*.txt", read=False)
		await stream.wait_processed()

		self.assertEqual(len(stream.files), 1)
		file = stream.files[0]

		self.assertIsInstance(file, pylp.File)
		self.assertEqual(file.path, abspath("fixtures/file.txt"))
		self.assertEqual(file.contents, "")

	
	async def test_src_deep_glob(self):
		"""It should return a stream from a deep glob"""

		files = [
			("fixtures/file.txt", "This is a test file."),
			("fixtures/some-files/file3.txt", "This is another test file.")
		]

		stream = pylp.src("fixtures/**/*.txt")
		await stream.wait_processed()

		self.assertEqual(len(stream.files), len(files))
		stream.files.sort(key=lambda f: f.path)
		files.sort(key=lambda x: x[0])

		for (path, contents), file in zip(files, stream.files):
			self.assertIsInstance(file, pylp.File)
			self.assertEqual(file.path, abspath(path))
			self.assertEqual(file.contents, contents)


	async def test_src_same_file(self):
		"""It should return a stream, with no duplicates"""

		files = [
			("fixtures/file.txt", "This is a test file."),
			("fixtures/some-files/file3.txt", "This is another test file.")
		]

		stream = pylp.src(["fixtures/**/*.txt", "fixtures/*.txt"])
		await stream.wait_processed()

		self.assertEqual(len(stream.files), len(files))

		for (path, contents), file in zip(files, stream.files):
			self.assertIsInstance(file, pylp.File)
			self.assertEqual(file.path, abspath(path))
			self.assertEqual(file.contents, contents)
