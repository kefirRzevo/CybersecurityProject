import os
import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent
sys.path.append((repo_path / "src").as_posix())

import wav_lsb_steganography

class TestWavLSBSteganography(unittest.TestCase):
    def setUp(self):
        self.input_file = repo_path / "res" / "videoplayback.wav"
        self.output_file = repo_path / "tmp" / "parsedplayback.wav"

    def tearDown(self):
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        msg = "hello world"
	
        wav_lsb_steganography.LSBWavEncode.encode(self.input_file, self.output_file, msg)
        res = wav_lsb_steganography.LSBWavDecode.decode(self.output_file)

        self.assertEqual(res, msg)

if __name__ == "__main__":
    unittest.main()
