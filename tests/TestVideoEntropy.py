import unittest
import os
import sys
import cv2

from pathlib import Path

repo_path = Path(__file__).parent.parent
sys.path.append((repo_path / "src").as_posix())

from video_entropy import *

class TestImgEntropy(unittest.TestCase):
  def test(self):
    img_path = repo_path / "res" / "puppy.png"
    img = cv2.imread(img_path)

    entropy = VideoEntropy.frame_entropy(img)
    print(entropy)


class TestVideoEntropy(unittest.TestCase):
  def test(self):
    video_path = repo_path / "res" / "videoplayback.mp4"
    video: ParsedVideo = VideoExtracter.extract(video_path)

    out_path = repo_path / "res" / "videoplayback_entropy.png"

    entropy_video = VideoEntropy(video.frames, video.fps)
    entropy_video.entropy_image(another=None, out=out_path)

class TestImageEntropyFeatured(unittest.TestCase):
  def test(self):
    img_path = repo_path / "res" / "puppy.png"
    out_img_path = repo_path / "res" / "puppy_entropy.png"
    img = cv2.imread(img_path)

    entropy = VideoEntropy.frame_entropy(img, p=3)
    plt.imshow(entropy, cmap="plasma", interpolation=None)
    plt.savefig(fname=out_img_path)

if __name__ == '__main__':
  unittest.main()