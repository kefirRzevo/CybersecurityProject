#!/usr/bin/python3

import cv2
import sys
import numpy as np
import scipy.io.wavfile as wv
from pydub import AudioSegment

def extract_frames(mp4_path):
    # Open the video file
    video = cv2.VideoCapture(mp4_path)
    
    if not video.isOpened():
        raise ValueError(f"Unable to open video file: {mp4_path}")
    
    frames = []
    frame_count = 0
    
    while True:
        ret, frame = video.read()
        if not ret:  # No more frames
            break
        frames.append(frame)  # Store frame
        frame_count += 1
    
    video.release()  # Release the video capture object
    print(f"Extracted {frame_count} frames from {mp4_path}")
    return frames

def extract_audio_with_pydub(mp4_path, wav_path):
  audio = AudioSegment.from_file(mp4_path, format="mp4")
  audio.export(wav_path, format="wav")
  print(f"Audio extracted to {wav_path}")

if __name__ == "__main__":
  frames = extract_frames(sys.argv[1])
  print(frames[0].shape)
  extract_audio_with_pydub(sys.argv[1], "tmp.wav")
  fs, x = wv.read("tmp.wav")
  print(x.shape)
