import sys
import unittest
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
sys.path.append((repo_path / "src").as_posix())

from parse_mov import ParsedVideo, VideoExtracter, VideoCombiner

class TestVideoParser(unittest.TestCase):
    def setUp(self):
        tmp_dir = repo_path / "tmp"
        if not tmp_dir.exists():
            tmp_dir.mkdir()
        self.input_file = repo_path / "data" / "video.mov"
        self.output_file = repo_path / "tmp" / "video_encoded.mov"

    def test(self):
        parsed: ParsedVideo = VideoExtracter.extract(self.input_file)
        VideoCombiner.combine(self.output_file, parsed)

if __name__ == "__main__":
    unittest.main()
