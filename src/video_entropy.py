import numpy as np
import scipy.stats as ss
from pathlib import Path
from video_parser import *
import matplotlib.pyplot as plt

class VideoEntropy:
  # frame_array: np.ndarray[np.ndarray[tuple[np.int8, np.int8, np.int8], tuple[int, int] ], int]

  def __init__(self, frames: list[np.ndarray], fps: int) -> None:
    self.frame_array = frames
    self.fps = fps
  
  def rect_entropy(frame: np.ndarray) -> float:
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
    hist, _ =np.histogram(
      frame, 
      bins=256, 
      range=(0, 256), 
      density=True)

    return ss.entropy(hist, base=2)
  
  def frame_entropy(frame: np.ndarray, p: int | None = None) -> np.ndarray | float:
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

    frame_flat = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).ravel()

    if p == None or p >= x_len or p >= y_len:
      return VideoEntropy.rect_entropy(frame_flat)

    if p < 1:
      raise ValueError(f"The period must be a value greater then 0, but period={p}")

    res = np.zeros(shape=(y_len, x_len))
    for x in range(p, x_len - p - 1):
      for y in range(p, y_len - p - 1):
        frame_flat = cv2.cvtColor(frame[y-p:y+p+1, x-p:x+p+1], cv2.COLOR_BGR2GRAY).ravel()
        res[y][x] = VideoEntropy.rect_entropy(frame_flat)
    
    return res
  
  def _featured_entropy_image(self, another: list[np.ndarray] | None, out: Path, period: int, fps: int) -> None:
    entropy_frames = []
    for i in range(len(self.frame_array)):
      entropy_tmp = VideoEntropy.frame_entropy(self.frame_array[i], period)
      if another is not None:
        another_frame_entropy = VideoEntropy.frame_entropy(another[i], period)
        entropy_tmp = np.abs(entropy_tmp - another_frame_entropy)
      
      print(i)
      img = plt.imshow(entropy_tmp, cmap="plasma", interpolation=None)
      frame = img.get_array()
      entropy_frames.append(frame)
      
    
    out_video = ParsedVideo
    out_video.fps = self.fps
    out_video.frames = entropy_frames

    VideoCombiner.combine(out_video, out)
  
  def entropy_image(self, another: list[np.ndarray] | None, out: Path, period: int | None = None) -> None:
    """
    Calculate total entropy for each frame and build a graph where on y axis 
    is entropy and on x axis is frame index if diff is `None`. if not, calculate total 
    entropy for both frame arrays and plot only theres difference
    """

    if another is not None and len(another) != len(self.frame_array):
      raise ValueError(f"number of frames in video passed with `--diff` [{len(another)}] must much "
                       f"number of frames in video passed with `--video` [{len(self.frame_array)}]")

    if period is not None:
      self._featured_entropy_image(another, out, period, self.fps)
      return
    
    entropy_y = [
      VideoEntropy.frame_entropy(self.frame_array[i]) - (
        VideoEntropy.frame_entropy(another[i]) 
        if another is not None and len(another) == len(self.frame_array) else 0
      ) 
      for i in range(0, len(self.frame_array))
    ]
    print(len(entropy_y))
    entropy_x = np.arange(len(self.frame_array))

    plt.figure(111, figsize=[12, 8])
    plt.plot(entropy_x, entropy_y, "b.", label="Total Entropy of every video frame")
    plt.ylabel("Entropy")
    plt.xlabel("Frame index")
    plt.savefig(fname=out)
