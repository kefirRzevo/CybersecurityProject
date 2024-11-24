#!/usr/bin/python3

import numpy as np

from logger import logger

class LSBFrame:
    def _index_to_i_j(pixels: np.ndarray, index: int) -> tuple[int, int]:
        cols = len(pixels[0])
        i = index // cols
        j = index % cols
        return i, j

    def _round_to_multiple_of_six(msg_len: int) -> int:
        return (msg_len + 5) // 6 * 6

class LSBFrameEncode(LSBFrame):
    def _set_data_in_pixel(pixels: np.ndarray, index: int, bin_bits: str):
        i, j = LSBFrame._index_to_i_j(pixels, index)
        pixels[i][j][0] &= 0b11111100  # Clear last 2 bits of channel 0
        pixels[i][j][1] &= 0b11111100  # Clear last 2 bits of channel 1
        pixels[i][j][2] &= 0b11111100  # Clear last 2 bits of channel 2
        pixels[i][j][0] |= int(bin_bits[0:2], 2)  # Set bits 0-1
        pixels[i][j][1] |= int(bin_bits[2:4], 2)  # Set bits 2-3
        pixels[i][j][2] |= int(bin_bits[4:6], 2)  # Set bits 4-5

    def encode(frame: np.ndarray, msg: str) -> np.ndarray:
        logger.info(f"Started encoding message '{msg}'")
        msg_len_bin = bin(len(msg))[2:].zfill(24)
        index = 0
        for i in range(0, 24, 6):
            LSBFrameEncode._set_data_in_pixel(frame, index, msg_len_bin[i:i + 6])
            index += 1

        # Convert each character of the message to an 8-bit binary string
        bits = "".join(bin(ord(char))[2:].zfill(8) for char in msg)
        bits_len = len(bits)
        
        # Pad the message binary string to be a multiple of 6
        dummy_count = LSBFrame._round_to_multiple_of_six(bits_len) - bits_len
        bits_res = "0" * dummy_count + bits
        bits_res_len = len(bits_res)

        # Embed the message binary data into the pixel data
        for i in range(0, bits_res_len, 6):
            LSBFrameEncode._set_data_in_pixel(frame, index, bits_res[i:i + 6])
            index += 1

        logger.info(f"Ended encoding message '{msg}'")
        return frame

class LSBFrameDecode(LSBFrame):
    def _get_data_from_pixel(pixels: np.ndarray, index: int) -> str:
        i, j = LSBFrame._index_to_i_j(pixels, index)
        temp = ""
        first_local = bin(pixels[i][j][0] & 3)[2:]
        first_local = (2 - len(first_local)) * "0" + first_local
        temp += first_local
        second_local = bin(pixels[i][j][1] & 3)[2:]
        second_local = (2 - len(second_local)) * "0" + second_local
        temp += second_local
        third_local = bin(pixels[i][j][2] & 3)[2:]
        third_local = (2 - len(third_local)) * "0" + third_local
        temp += third_local
        return temp

    def decode(pixels: np.ndarray) -> str:
        logger.info(f"Started decoding message")
        msg_len_bin = ""
        index = 0
        for _ in range(4):  # Read 4 pixels for 24 bits
            msg_len_bin += LSBFrameDecode._get_data_from_pixel(pixels, index)
            index += 1

        bits_len = int(msg_len_bin, 2) * 8
        bits_res_len = LSBFrame._round_to_multiple_of_six(bits_len)

        bits_res = ""
        for _ in range(bits_res_len // 6):
            bits_res += LSBFrameDecode._get_data_from_pixel(pixels, index)
            index += 1

        msg = ""
        bits = bits_res[(bits_res_len-bits_len):]
        bits_len = len(bits)

        for i in range(0, bits_len, 8):
            byte = bits[i:i + 8]
            msg += chr(int(byte, 2))
        
        logger.info(f"Ended decoding message '{msg}'")
        return msg
