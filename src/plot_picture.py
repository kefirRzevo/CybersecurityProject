import numpy as np
import cv2
import scipy.stats as ss
from pathlib import Path
from parse_mov import ParsedVideo, VideoExtracter, VideoCombiner
import matplotlib.pyplot as plt

from logger import logger

def _rect_entropy(frame: np.ndarray) -> float:
	"""
	for given frame calculate entropy of rectangle erased from frame.

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

def _video_entropy(path_to_video: Path) -> np.ndarray:
	parsed: ParsedVideo = VideoExtracter.extract(path_to_video)
	logger.info(f"Started getting video entropy {path_to_video}")
	frames_etropy = []
	for i in range(parsed.frames_count):
		path_to_frame = parsed.path_to_frame(i)
		img = cv2.imread(path_to_frame.as_posix())
		frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
		frames_etropy.append(_rect_entropy(frame))

	return frames_etropy

def plot_video(path_to_video: Path, path_to_output: Path):
	entropy_y = _video_entropy(path_to_video)
	entropy_x = np.arange(len(entropy_y))

	plt.figure(111, figsize=[12, 8])
	plt.plot(entropy_x, entropy_y, "b.", label="Total Entropy of every video frame")
	plt.ylabel("Entropy")
	plt.xlabel("Frame index")
	plt.savefig(fname=path_to_output)

def plot_video_diff(path_to_lhs: Path, path_to_rhs: Path, path_to_output: Path):
	logger.info(f"Started plot lhs video entropy {path_to_lhs}")
	entropy_lhs = _video_entropy(path_to_lhs)
	logger.info(f"Started plot rhs video entropy {path_to_rhs}")
	entropy_rhs = _video_entropy(path_to_rhs)
	logger.info(f"Getting res video entropy")
	entropy_y = [lhs - rhs for lhs, rhs in zip(entropy_lhs, entropy_rhs)]
	entropy_x = np.arange(len(entropy_y))

	plt.figure(111, figsize=[12, 8])
	plt.plot(entropy_x, entropy_y, "b.", label="Total Entropy of every video frame")
	plt.ylabel("Entropy")
	plt.xlabel("Frame index")
	plt.savefig(fname=path_to_output)

def plot_picture(path_to_picture: Path, path_to_output: Path):
	logger.info(f"Started plot picture entropy {path_to_picture}")
	img = cv2.imread(path_to_picture.as_posix())
	frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
	entropy = _frame_entropy(frame)
	plt.imshow(entropy, cmap="plasma", interpolation=None)
	plt.savefig(fname=path_to_output.as_posix())

def plot_picture_diff(lhs: Path, rhs: Path, path_to_output: Path) -> None:
	logger.info(f"Started plot lhs picture entropy {lhs}")
	lhs_img = cv2.imread(lhs.as_posix())
	lhs_frame = cv2.cvtColor(lhs_img, cv2.COLOR_BGRA2BGR)
	lhs_entropy = _frame_entropy(lhs_frame)

	logger.info(f"Started plot rhs picture entropy {rhs}")
	rhs_img = cv2.imread(rhs.as_posix())
	rhs_frame = cv2.cvtColor(rhs_img, cv2.COLOR_BGRA2BGR)
	rhs_entropy = _frame_entropy(rhs_frame)

	logger.info(f"Getting res picture entropy")
	entropy = np.abs(lhs_entropy - rhs_entropy)
	plt.imshow(entropy, cmap="plasma", interpolation=None)
	plt.savefig(fname=path_to_output.as_posix())
