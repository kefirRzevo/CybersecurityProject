import cv2
from lsb_frame_steganography import LSBFrameEncode, LSBFrameDecode

from pathlib import Path
from logger import logger

class LSBPngEncode():
    def encode_max_len(path_to_input: Path) -> int:
        img = cv2.imread(path_to_input.as_posix())
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return LSBFrameEncode.encode_max_len(frame)

    def encode(path_to_input: Path, path_to_output: Path, msg: str):
        max_len = LSBPngEncode.encode_max_len(path_to_input)
        logger.info(f"Max length to encode in the png '{max_len}'")
        if len(msg) > max_len:
            raise Exception("too large message")
        logger.info(f"Started encoding message '{msg}'")
        img = cv2.imread(path_to_input.as_posix())
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        encoded = LSBFrameEncode.encode(frame, msg)
        cv2.imwrite(path_to_output.as_posix(), encoded)
        logger.info(f"Ended encoding message '{msg}'")

class LSBPngDecode():
    def decode(path_to_input: Path) -> str:
        logger.info(f"Started decoding message")
        img = cv2.imread(path_to_input.as_posix())
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        msg = LSBFrameDecode.decode(frame)
        logger.info(f"Ended decoding message '{msg}'")
        return msg
