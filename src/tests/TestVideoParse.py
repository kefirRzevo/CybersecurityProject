import os
import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

from video_parser import VideoExtracter, VideoCombiner

class TestVideoParser(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "res" / "videoplayback.mp4"
        self.output_file = repo_path / "tmp" / "parsedplayback.mp4"

    def tearDown(self):
        if self.output_file.exists():
            os.remove(self.output_file)

    def test(self):
        parsed = VideoExtracter.extract(self.input_file)
        VideoCombiner.combine(self.output_file, parsed)

if __name__ == "__main__":
    unittest.main()
