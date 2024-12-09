import os
import sys
import unittest
import cv2
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

from lsb_tiff_steganography import LSBTiffEncode, LSBTiffDecode

class TestTiffLSBSteganography(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "res" / "puppy.tiff"
        self.output_file = repo_path / "tmp" / "puppy_encoded.tiff"
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        msg = "hell"
        LSBTiffEncode.encode(self.input_file, self.output_file, msg)
        res = LSBTiffDecode.decode(self.output_file)
        self.assertEqual(res, msg)

if __name__ == "__main__":
    unittest.main()
