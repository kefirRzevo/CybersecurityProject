import os
import sys
import unittest
import cv2
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

from frame_lsb_steganography import LSBFrameEncode, LSBFrameDecode

class TestFrameLSBSteganography(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "res" / "puppy.png"
        self.output_file = repo_path / "tmp" / "puppy_encoded.png"
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        img = cv2.imread(self.input_file.as_posix())
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        msg = "hell"
        encoded_frame = LSBFrameEncode.encode(frame, msg)
        cv2.imwrite(self.output_file.as_posix(), frame)
        res = LSBFrameDecode.decode(encoded_frame)

        self.assertEqual(res, msg)

if __name__ == "__main__":
    unittest.main()
