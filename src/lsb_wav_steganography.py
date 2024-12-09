import wave
from pathlib import Path

from lsb_bytes_steganography import LSBBytesEncode, LSBBytesDecode

from logger import logger

class LSBWavEncode():
    def encode_max_len(path_to_input: Path):
        audio = wave.open(path_to_input.as_posix(), mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        return LSBBytesEncode.encode_max_len(frame_bytes)

    def encode(path_to_input: Path, path_to_output: Path, msg: str):
        """
        Encodes a secret message into an audio file using basic LSB steganography with message length.

        :param path_to_input: Path to the input audio file
        :param path_to_output: Path to the output encoded audio file
        :param msg: The message to be encoded
        """
        max_len = LSBWavEncode.encode_max_len(path_to_input)
        logger.info(f"Max length to encode in the wav '{max_len}'")
        if len(msg) > max_len:
            raise Exception("too large message")

        logger.info("Encoding starts...")
        audio = wave.open(path_to_input.as_posix(), mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        frame_bytes = LSBBytesEncode.encode(frame_bytes, msg)
        frame_modified = bytes(frame_bytes)

        # Write the modified bytes to the new audio file
        with wave.open(path_to_output.as_posix(), "wb") as new_audio:
            new_audio.setparams(audio.getparams())
            new_audio.writeframes(frame_modified)

        audio.close()
        logger.info(f"Successfully encoded into {path_to_output}")

class LSBWavDecode():
    def decode(path_to_input: Path) -> str:
        """
        Decodes a secret message from an audio file using basic LSB steganography with message length.

        :param path_to_input: Path to the encoded audio file
        :return: The decoded secret message
        """
        logger.info("Decoding starts...")
        audio = wave.open(path_to_input.as_posix(), mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        return LSBBytesDecode.decode(frame_bytes)
