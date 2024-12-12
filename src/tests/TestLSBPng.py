import os
import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

from lsb_png_steganography import LSBPngEncode, LSBPngDecode

class TestPngLSBSteganography(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "data" / "puppy.png"
        self.output_file = repo_path / "tmp" / "puppy_encoded.png"
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        msg = "hell"
        LSBPngEncode.encode(self.input_file, self.output_file, msg)
        res = LSBPngDecode.decode(self.output_file)
        self.assertEqual(res, msg)

if __name__ == "__main__":
    unittest.main()
