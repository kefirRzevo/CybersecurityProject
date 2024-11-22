import os
import unittest

from ...src import wav_lsb_steganography

class TestWavLSBSteganography(unittest.TestCase):
    def setUp(self):
        self.input_file = 'audio.wav'
        self.output_file = 'output.wav'

    def tearDown(self):
        os.remove(self.output_file)

    def test(self):
        msg = 'hello world'
	
        wav_lsb_steganography.encode(self.input_file, self.output_file, msg)
        res = wav_lsb_steganography.decode(self.output_file)

        self.assertEqual(res, msg)

if __name__ == '__main__':
    unittest.main()
