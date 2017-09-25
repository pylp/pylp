"""

Test transformers contained in streams.

Copyright (C) 2017 The Pylp Authors.
This file is under the MIT License.

"""

import pylp
from utils import AsyncTestCase


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



class TestTransformer(AsyncTestCase):
	"""Test transformers contained in streams."""

	async def test_transfomer_upper(self):
		"""It should capitalize contents."""

		stream = pylp.src("./fixtures/file.txt").pipe(UpperTransformer())
		await stream.wait_processed()

		self.assertEqual(len(stream.files), 1)
		file = stream.files[0]

		self.assertIsInstance(file, pylp.File)
		self.assertEqual(file.contents, "THIS IS A TEST FILE.")

	
	async def test_transfomer_multiple(self):
		"""It should run multiple transformers."""

		recorder = RecorderTransformer()
		stream = pylp.pipes(
			pylp.src("./fixtures/file.txt"),
			UpperTransformer(),
			recorder,
			ReverseTransformer()
		)

		await stream.wait_processed()

		self.assertEqual(len(stream.files), 1)
		self.assertEqual(len(recorder.files), 1)

		self.assertEqual(recorder.files[0].contents, "THIS IS A TEST FILE.")
		self.assertEqual(stream.files[0].contents, ".ELIF TSET A SI SIHT")
