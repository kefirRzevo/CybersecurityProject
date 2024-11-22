import os
import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

import video_parser

class TestVideoParser(unittest.TestCase):
    def setUp(self):
        self.input_file = repo_path / "res" / "videoplayback.mp4"
        self.output_file = repo_path / "tmp" / "parsedplayback.mp4"

    def tearDown(self):
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        parsed = video_parser.VideoExtracter.extract(self.input_file)
        video_parser.VideoCombiner.combine(self.output_file, parsed)

if __name__ == "__main__":
    unittest.main()
