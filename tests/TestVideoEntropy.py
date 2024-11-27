import unittest
import os
import sys
import cv2

from pathlib import Path
from video_entropy import *

repo_path = Path(__file__).parent.parent
sys.path.append((repo_path / "src").as_posix())

class TestImgEntropy(unittest.TestCase):
  def test(self):
    img_path = repo_path / "res" / "puppy.png"
    img = cv2.imread(img_path)
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    


class TestVideoEntropy(unittest.TestCase):
  def setUp(self):
    pass

  def test(self):
    pass

class TestVideoEntropyFeatured(unittest.TestCase):
  def setUp(self):
    pass

  def test(self):
    pass

if __name__ == '__main__':
  unittest.main()