import wave
import struct
from pathlib import Path

from logger import logger

class LSBWavEncode():
    def encode(path_to_input: Path, path_to_output: Path, msg: str):
        """
        Encodes a secret message into an audio file using basic LSB steganography with message length.

        :param path_to_input: Path to the input audio file
        :param path_to_output: Path to the output encoded audio file
        :param msg: The message to be encoded
        """
        try:
            logger.info("Encoding starts...")
            audio = wave.open(path_to_input.as_posix(), mode="rb")
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

            logger.info(f"Secret message: {msg}")
            # Convert the secret message to bits
            msg_bits = "".join([bin(ord(i)).lstrip("0b").rjust(8, "0") for i in msg])
            message_length = len(msg_bits)

            # Pack the length of the message into 4 bytes (32 bits)
            length_bytes = struct.pack(">I", message_length)  # ">I" is big-endian unsigned int

            # Convert the length bytes to bits
            length_bits = "".join([bin(byte).lstrip("0b").rjust(8, "0") for byte in length_bytes])

            # Combine length bits and message bits
            full_bits = length_bits + msg_bits

            # Ensure the message fits into the frame bytes
            if len(full_bits) > len(frame_bytes):
                raise ValueError("The secret message is too large to fit in the audio file.")

            # Encode the full bits into the frame bytes
            for i, bit in enumerate(full_bits):
                frame_bytes[i] = (frame_bytes[i] & 254) | int(bit)

            frame_modified = bytes(frame_bytes)

            # Write the modified bytes to the new audio file
            with wave.open(path_to_output.as_posix(), "wb") as new_audio:
                new_audio.setparams(audio.getparams())
                new_audio.writeframes(frame_modified)

            audio.close()
            logger.info(f"Successfully encoded into {path_to_output}")
        except Exception as e:
            logger.error(f"Error during encoding: {e}")

class LSBWavDecode():
    def decode(path_to_input: Path):
        """
        Decodes a secret message from an audio file using basic LSB steganography with message length.

        :param path_to_input: Path to the encoded audio file
        :return: The decoded secret message
        """
        try:
            logger.info("Decoding starts...")
            audio = wave.open(path_to_input.as_posix(), mode="rb")
            frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))

            # Extract the first 32 bits to determine the message length
            length_bits = "".join([str((frame_bytes[i] & 1)) for i in range(32)])
            message_length = struct.unpack(">I", int(length_bits, 2).to_bytes(4, byteorder="big"))[0]

            logger.info(f"Extracted message length: {message_length} bits")

            # Now extract the message bits using the extracted length
            if message_length > len(frame_bytes) * 8:
                raise ValueError("The extracted message length is larger than the available audio data.")

            message_bits = "".join([str((frame_bytes[i + 32] & 1)) for i in range(message_length)])

            # Convert bits back to characters
            decoded_message = "".join(chr(int(message_bits[i:i + 8], 2)) for i in range(0, len(message_bits), 8))

            logger.info(f"Successfully decoded: {decoded_message}")
            audio.close()
            return decoded_message

        except Exception as e:
            logger.error(f"Error during decoding: {e}")
            return None
