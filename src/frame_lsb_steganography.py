#!/usr/bin/python3

import numpy as np
from video_parser import ParsedVideo
from PIL import Image, ImageMath

from logger import logger

class LSBFrame:
    bits: int
    frame: np.ndarray

class LSBFrameEncode():
    def encode(self, frame: LSBFrame, secret: str):
        c = self.cover.split()
        print(type(c))
        s = self.secret.split()
        print(type(s))
        expr = "convert((c & (256 - 2**bits)) + ((s & (256 - 2**(8 - bits)) - 1) >> (8 - bits)), 'L')"
        out = [ImageMath.eval(expr, c = c[k], s = s[k], bits = self.bits) for k in range(len(c))]
        out = Image.merge(self.cover.mode, out)
        self.cover.paste(out, (0, 0))
        self._save_img(self.cover, self.outfile)
        print(f'[*] Created outfile at {self.outfile}')

class LSBFrameDecode():
    def decode(frame: LSBFrame) -> str:
        s = self.steg.split()
        expr = 'convert((s & 2**bits - 1) << (8 - bits), "L")'
        out = [ImageMath.eval(expr, s = s[k], bits = self.bits) for k in range(len(s))] 
        out = Image.merge(self.steg.mode, out)
        self._save_img(out, self.outfile)
        print(f'[*] Created outfile at {self.outfile}')
