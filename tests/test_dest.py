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

@pytest.mark.asyncio
class TestDestTransformer:
    """Test 'pylp.dest' for writing contents to local files."""

    def setup_method(self, test_method):
        self.out_folder = "tests/out-fixtures/"

        shutil.rmtree(self.out_folder, ignore_errors=True)
        os.mkdir(self.out_folder)

    def teardown_method(self):
        shutil.rmtree(self.out_folder, ignore_errors=True)

    async def test_dest_simple(self):
        """It should return a writing transformer"""

        transformer = pylp.dest("tests/fixtures/")
        assert isinstance(transformer, FileWriter)


    async def test_dest_copy(self):
        """It should copy a file into the destination folder"""

        stream = pylp.src("tests/fixtures/*.txt").pipe(pylp.dest(self.out_folder))
        await stream.wait_processed()

        filename = path.join(self.out_folder, "file.txt")

        assert path.isfile(filename)

        with open(filename, "r") as file:
            assert file.read() == "This is a test file."


    async def test_dest_copy_base(self):
        """It should copy a file into the destination folder, keeping the base folder"""

        stream = pylp.src("tests/fixtures/**/*.ext2").pipe(pylp.dest(self.out_folder))
        await stream.wait_processed()

        filename = path.join(self.out_folder, "other-files/a-file.ext2")
        assert path.isfile(filename)

        with open(filename, "r") as file:
            assert file.read(), "A file in a folder."
