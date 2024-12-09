import struct
import numpy as np
from pathlib import Path

from logger import logger

class LSBBytesEncode():
    def encode_max_len(frame_bytes: np.array):
        return len(frame_bytes) // 8

    def encode(frame_bytes: np.array, msg: str) -> np.array:
        max_len = LSBBytesEncode.encode_max_len(frame_bytes)
        logger.info(f"Max length to encode in the frame '{max_len}'")
        if len(msg) > max_len:
            raise Exception("too large message")

        logger.info(f"Started encoding message '{msg}'")
        # Convert the secret message to bits
        msg_bits = "".join([bin(ord(i)).lstrip("0b").rjust(8, "0") for i in msg])
        message_length = len(msg_bits)

        # Pack the length of the message into 4 bytes (32 bits)
        length_bytes = struct.pack(">I", message_length)  # ">I" is big-endian unsigned int

        # Convert the length bytes to bits
        length_bits = "".join([bin(byte).lstrip("0b").rjust(8, "0") for byte in length_bytes])

        # Combine length bits and message bits
        full_bits = length_bits + msg_bits

        # Encode the full bits into the frame bytes
        for i, bit in enumerate(full_bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | int(bit)

        logger.info(f"Ended encoding message '{msg}'")
        return frame_bytes

class LSBBytesDecode():
    def decode(frame_bytes: np.array) -> str:
        logger.info(f"Started decoding message")

        # Extract the first 32 bits to determine the message length
        length_bits = "".join([str((frame_bytes[i] & 1)) for i in range(32)])
        message_length = struct.unpack(">I", int(length_bits, 2).to_bytes(4, byteorder="big"))[0]

        logger.info(f"Extracted message length: {message_length // 8} bytes")

        # Now extract the message bits using the extracted length
        message_bits = "".join([str((frame_bytes[i + 32] & 1)) for i in range(message_length)])

        # Convert bits back to characters
        decoded_message = "".join(chr(int(message_bits[i:i + 8], 2)) for i in range(0, len(message_bits), 8))

        logger.info(f"Ended decoding message '{decoded_message}'")
        return decoded_message
