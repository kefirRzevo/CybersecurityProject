import numpy as np
import cv2
import scipy.stats as ss
from pathlib import Path
from parse_mov import ParsedVideo, VideoExtracter, VideoCombiner
import matplotlib.pyplot as plt

def _rect_entropy(frame: np.ndarray) -> float:
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
	hist, _ = np.histogram(
	frame, 
	bins=256, 
	range=(0, 256), 
	density=True)
	return ss.entropy(hist, base=2)

def _frame_entropy(frame: np.ndarray) -> float:
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
	res = np.zeros(shape=(y_len, x_len))
	p = 3
	for x in range(p, x_len - p - 1):
		for y in range(p, y_len - p - 1):
			frame_flat = cv2.cvtColor(frame[y-p:y+p+1, x-p:x+p+1], cv2.COLOR_BGR2GRAY).ravel()
			res[y][x] = _rect_entropy(frame_flat)
	return res

def plot_video(path_to_video: Path, path_to_output: Path):
	parsed: ParsedVideo = VideoExtracter.extract(path_to_video)
	frames: list[np.ndarray] = []
	for i in range(parsed.frames_count):
		path_to_frame = parsed.path_to_frame(i)
		img = cv2.imread(path_to_frame.as_posix())
		frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
		frames.append(frame)
	pass

def plot_video_diff(path_to_lhs: Path, path_to_rhs: Path, path_to_output: Path):
	pass

# def _featured_entropy_image(self, another: list[np.ndarray] | None, out: Path, period: int, fps: int) -> None:
# 	entropy_frames = []
# 	for i in range(len(self.frame_array)):
# 		entropy_tmp = PictureEntropy.frame_entropy(self.frame_array[i], period)
# 		if another is not None:
# 			another_frame_entropy = PictureEntropy.frame_entropy(another[i], period)
# 			entropy_tmp = np.abs(entropy_tmp - another_frame_entropy)
	
# 	print(i)
# 	img = plt.imshow(entropy_tmp, cmap="plasma", interpolation=None)
# 	frame = img.get_array()
# 	entropy_frames.append(frame)
	
	
# 	out_video = ParsedVideo
# 	out_video.fps = fps
# 	out_video.frames = entropy_frames

# 	VideoCombiner.combine(out_video, out)

# def entropy_image(self, another: list[np.ndarray] | None, out: Path, period: int | None = None) -> None:
# 	"""
# 	Calculate total entropy for each frame and build a graph where on y axis
# 	is entropy and on x axis is frame index if diff is `None`. if not, calculate total
# 	entropy for both frame arrays and plot only theres difference
# 	"""

# 	if another is not None and len(another) != len(self.frame_array):
# 		raise ValueError(f"number of frames in video passed with `--diff` [{len(another)}] must much "
# 						f"number of frames in video passed with `--video` [{len(self.frame_array)}]")

# 	if period is not None:
# 		self._featured_entropy_image(another, out, period, self.fps)
# 		return

# 	entropy_y = [
# 		PictureEntropy.frame_entropy(self.frame_array[i]) - (
# 			PictureEntropy.frame_entropy(another[i]) 
# 			if another is not None and len(another) == len(self.frame_array) else 0
# 		) 
# 		for i in range(0, len(self.frame_array))
# 	]
# 	print(len(entropy_y))
# 	entropy_x = np.arange(len(self.frame_array))

# 	plt.figure(111, figsize=[12, 8])
# 	plt.plot(entropy_x, entropy_y, "b.", label="Total Entropy of every video frame")
# 	plt.ylabel("Entropy")
# 	plt.xlabel("Frame index")
# 	plt.savefig(fname=out)

def plot_picture(path_to_picture: Path, path_to_output: Path):
	img = cv2.imread(path_to_picture.as_posix())
	frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
	entropy = _frame_entropy(frame)
	plt.imshow(entropy, cmap="plasma", interpolation=None)
	plt.savefig(fname=path_to_output.as_posix())

def plot_picture_diff(lhs: Path, rhs: Path, path_to_output: Path) -> None:
	lhs_img = cv2.imread(lhs.as_posix())
	lhs_frame = cv2.cvtColor(lhs_img, cv2.COLOR_BGRA2BGR)
	lhs_entropy = _frame_entropy(lhs_frame)

	rhs_img = cv2.imread(rhs.as_posix())
	rhs_frame = cv2.cvtColor(rhs_img, cv2.COLOR_BGRA2BGR)
	rhs_entropy = _frame_entropy(rhs_frame)

	entropy = np.abs(lhs_entropy - rhs_entropy)
	plt.imshow(entropy, cmap="plasma", interpolation=None)
	plt.savefig(fname=path_to_output.as_posix())
