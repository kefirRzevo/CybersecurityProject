import soundfile as sf  
from pathlib import Path

from lsb_bytes_steganography import LSBBytesEncode, LSBBytesDecode

from logger import logger

class LSBFlacEncode():
		def encode_max_len(path_to_input: Path):
				frame_bytes, samplerate = sf.read(path_to_input.as_posix(), dtype="int16")
				return LSBBytesEncode.encode_max_len(frame_bytes)

		def encode(path_to_input: Path, path_to_output: Path, msg: str):
				"""
				Encodes a secret message into an audio file using basic LSB steganography with message length.

				:param path_to_input: Path to the input audio file
				:param path_to_output: Path to the output encoded audio file
				:param msg: The message to be encoded
				"""
				max_len = LSBFlacEncode.encode_max_len(path_to_input)
				logger.info(f"Max length to encode in the wav '{max_len}'")
				if len(msg) > max_len:
						raise Exception("too large message")

				logger.info("Encoding starts...")
				frame_bytes, samplerate = sf.read(path_to_input.as_posix(), dtype="int16")
				print(type(frame_bytes[0]))
				frame_bytes = LSBBytesEncode.encode(frame_bytes, msg)

				# Write the modified bytes to the new audio file 
				sf.write(path_to_output.as_posix(), frame_bytes, samplerate)
				logger.info(f"Successfully encoded into {path_to_output}")

class LSBFlacDecode():
		def decode(path_to_input: Path) -> str:
				"""
				Decodes a secret message from an audio file using basic LSB steganography with message length.

				:param path_to_input: Path to the encoded audio file
				:return: The decoded secret message
				"""
				logger.info("Decoding starts...")
				frame_bytes, samplerate = sf.read(path_to_input.as_posix(), dtype="int16")
				return LSBBytesDecode.decode(frame_bytes)
