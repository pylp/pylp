"""

Test 'pylp.dest' for writing contents to local files.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import os, os.path as path
import shutil
import pylp
from pylp.lib.dest import FileWriter
from utils import AsyncTestCase


class TestDestTransformer(AsyncTestCase):
	"""Test 'pylp.dest' for writing contents to local files."""

	def setUp(self):
		self.out_folder = "./out-fixtures/"
		
		shutil.rmtree(self.out_folder, ignore_errors=True)
		os.mkdir(self.out_folder)


	def test_dest_simple(self):
		"""It should return a writing transformer"""

		transformer = pylp.dest("./fixtures/")
		self.assertIsInstance(transformer, FileWriter)

	
	async def test_dest_copy(self):
		"""It should copy a file into the destination folder"""

		stream = pylp.src("./fixtures/*.txt").pipe(pylp.dest(self.out_folder))
		await stream.wait_processed()

		filename = path.join(self.out_folder, "file.txt")
		self.assertTrue(path.isfile(filename))

		with open(filename, "r") as file:
			self.assertEqual(file.read(), "This is a test file.")


	async def test_dest_copy_base(self):
		"""It should copy a file into the destination folder, keeping the base folder"""

		stream = pylp.src("./fixtures/**/*.ext2").pipe(pylp.dest(self.out_folder))
		await stream.wait_processed()

		filename = path.join(self.out_folder, "other-files/a-file.ext2")
		self.assertTrue(path.isfile(filename))

		with open(filename, "r") as file:
			self.assertEqual(file.read(), "A file in a folder.")
