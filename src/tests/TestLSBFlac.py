import os
import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

from lsb_flac_steganography import LSBFlacDecode, LSBFlacEncode

class TestFlacLSBSteganography(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "res" / "audio.flac"
        self.output_file = repo_path / "tmp" / "audio_encoded.flac"
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        msg = "hello world"
        LSBFlacEncode.encode(self.input_file, self.output_file, msg)
        res = LSBFlacDecode.decode(self.output_file)
        self.assertEqual(res, msg)

if __name__ == "__main__":
    unittest.main()
