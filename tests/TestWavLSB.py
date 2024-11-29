import os
import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent
sys.path.append((repo_path / "src").as_posix())

from wav_lsb_steganography import LSBWavDecode, LSBWavEncode

class TestWavLSBSteganography(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "res" / "videoplayback.wav"
        self.output_file = repo_path / "tmp" / "parsedplayback.wav"

    def tearDown(self):
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        with open(repo_path / "res" / "faust.txt") as f:
            msg = f.read()

        LSBWavEncode.encode(self.input_file, self.output_file, msg)
        res = LSBWavDecode.decode(self.output_file)

        self.assertEqual(res, msg)

if __name__ == "__main__":
    unittest.main()
