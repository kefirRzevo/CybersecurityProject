import matplotlib.pyplot as plt
from lsb_frame_steganography import LSBFrameEncode, LSBFrameDecode

from PIL import Image
from pathlib import Path
from logger import logger

class LSBTiffEncode():
	def encode_max_len(path_to_input: Path) -> int:
		frame = plt.imread(path_to_input.as_posix())
		return LSBFrameEncode.encode_max_len(frame)

	def encode(path_to_input: Path, path_to_output: Path, msg: str):
		max_len = LSBTiffEncode.encode_max_len(path_to_input)
		logger.info(f"Max length to encode in the tiff '{max_len}'")
		if len(msg) > max_len:
			raise Exception("too large message")
		logger.info(f"Started encoding message '{msg}'")
		frame = plt.imread(path_to_input.as_posix())
		encoded = LSBFrameEncode.encode(frame, msg)
		plt.imsave(path_to_output.as_posix(), encoded)
		logger.info(f"Ended encoding message '{msg}'")

class LSBTiffDecode():
	def decode(path_to_input: Path) -> str:
		logger.info(f"Started decoding message")
		frame = plt.imread(path_to_input.as_posix())
		msg = LSBFrameDecode.decode(frame)
		logger.info(f"Ended decoding message '{msg}'")
		return msg
