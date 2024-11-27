import numpy as np
import scipy.stats as ss
from pathlib import Path
from video_parser import *
import matplotlib.pyplot as plt

class VideoEntropy:
  # frame_array: np.ndarray[np.ndarray[tuple[np.int8, np.int8, np.int8], tuple[int, int] ], int]

  def __init__(self, frames: list[np.ndarray]) -> None:
    self.frame_array = frames
  
  def rect_entropy(frame: np.ndarray, x_A: int, y_A: int, x_B: int, y_B: int) -> float:
    """
    for given frame = `frames[frame_index]` calculate entropy of rectangle erased from frame.
    
   A________________________
    |        |             |
    |        |             |
    |        |             |
    |________|             |
    |        B             |
    |                      |
    |                      |
    |______________________| 

    So only the entropy of rectangle, stricted with vertexes A and B, is calculated.
    x_A, x_B, y_A, y_B must be valid pixel cooradinates.
    """
    return ss.entropy(np.histogram(frame[y_A:y_B][x_A:x_B], bins=256, range=range(0, 256), density=True)[0], base=2)
  
  def frame_entropy(frame: np.ndarray, p: int | None) -> np.ndarray | float:
    """
    Create a frame which illustrates the `frames[idx]` entropy

    :param idx: index of interested video frame
    :param p: "period" of entropy, minimal amount of pixels in image slice to 
    calculate local (see `rect_entropy()`) entropy. If `p=None` then entropy calculated 
    for the whole frame and returned value is just a float number.

    Be aware that resulting frame shape could be different from original frame shape.
    Recomended to use `p=None` because of slow computation 
    """
    x_len = len(frame[0])
    y_len = len(frame)

    if type(p) == None or p >= x_len or p >= y_len:
      return VideoEntropy.rect_entropy(frame, 0, 0, x_len, y_len)

    if p < 1:
      raise ValueError(f"The period must be a value greater then 0, but period={p}")

    res = np.zeros(y_len, x_len)
    for x in range(p, x_len - p):
      for y in range(p, y_len - p):
        res[y][x] = VideoEntropy.rect_entropy(frame, x - p, x + p + 1, y - p, y + p + 1)
    
    return res
  
  def default_entropy_diff_image(self, another: list[np.ndarray] | None, out: Path) -> None:
    """
    Calculate total entropy for each frame and build a graph where on y axis 
    is entropy and on x axis is frame index if diff is `None`. if not, calculate total 
    entropy for both frame arrays and plot only theres difference
    """
    entropy_y = np.ndarray([
      VideoEntropy.frame_entropy(self.frame_array[i]) - (
        VideoEntropy.frame_entropy(another[i]) if another is not None else 0
      ) 
      for i in range(0, len(self.frame_array))
    ])
    entropy_x = np.arange(len(self.frame_array))

    plt.figure(111, figsize=[12, 8])
    plt.plot(entropy_x, entropy_y, "b.", label="Total Entropy of every video frame")
    plt.ylabel("Entropy")
    plt.xlabel("Frame index")
    plt.savefig(fpath=out)
  
  def default_entropy_diff_image(self, another: list[np.ndarray], out: Path) -> None:
    entropy_y = np.ndarray([self.frame_entropy(i) for i in range(0, len(self.frame_array))])
    entropy_x = np.arange(len(self.frame_array))

    plt.figure(111, figsize=[12, 8])
    plt.plot(entropy_x, entropy_y, "b.", label="Total Entropy of every video frame")
    plt.ylabel("Entropy")
    plt.xlabel("Frame index")
    plt.savefig(fpath=out)
    pass

  def featured_entropy_show_create_video(self, period: int, out_path: Path) -> None:
    frames = []
    video = VideoExtracter.extract()
    pass
    # ХЗ как эту херню сделать
    