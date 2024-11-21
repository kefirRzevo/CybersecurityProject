#!/usr/bin/python3

import cv2
import sys
import numpy as np
import scipy.io.wavfile as wv
from pydub import AudioSegment
from pathlib import Path
import argparse
from moviepy import VideoFileClip, AudioFileClip
import subprocess

def extract_frames(mp4_path: Path):
    # Open the video file
    video = cv2.VideoCapture(mp4_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    codec = video.get(cv2.CAP_PROP_FOURCC)

    
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
    return frames, fps, int(codec)

def extract_audio_with_pydub(mp4_path, wav_path):
  audio = AudioSegment.from_file(mp4_path, format="mp4")
  audio.export(wav_path, format="wav")
  print(f"Audio extracted to {wav_path}")

def create_video_from_frames(frames, output_video_path, fps, codec):
  # Get the dimensions of the frames
  height, width, _ = frames[0].shape
  # Define the video codec and create a VideoWriter object
  fourcc = cv2.VideoWriter.fourcc(*'vp09')
  video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
  
  # Write each frame to the video
  for frame in frames:
      video_writer.write(frame)
  
  video_writer.release()
  print(f"Video created at {output_video_path}")

def combine_video_audio(video_path, audio_path, output_path, fps):
  # Load the video file
  video_clip = VideoFileClip(video_path)
  
  # Load the audio file
  audio_clip = AudioFileClip(audio_path)
  
  # Set the audio of the video clip to the loaded audio
  video_clip.with_audio(audio_clip)
  
  # Write the final video with sound to the output file
  video_clip.write_videofile(output_path, codec='vp09', audio_codec='aac')

  print(f"Video with audio saved as {output_path}")

def combine_video_audio_ffmpeg(video_path, audio_path, output_path):
    command = [
        "ffmpeg",
        "-i", video_path,   # Input video file
        "-i", audio_path,   # Input audio file
        "-c:v", "copy",     # Copy video codec (no re-encoding)
        output_path         # Output file path
    ]
    
    subprocess.run(command, check=True)
    print(f"Video with audio saved as {output_path}")

if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  # parser.add_argument('--video', required=True, help='path to video')
  # parser.add_argument('--secret', help='path to secret file')
  # parser.add_argument('--output', help='path to output video')
  # args = parser.parse_args()
  # video_path: Path = args.video
  # secret_path: Path = args.secret
  # output_path: Path = args.output
  
  frames, fps, codec = extract_frames(sys.argv[1])

  print(frames[0].shape)
  print(fps)
  extract_audio_with_pydub(sys.argv[1], "tmp.wav")
  fs, x = wv.read("tmp.wav")
  print(x.shape)


  # assembling frame array and wav audio array

  create_video_from_frames(frames, "res/tmp.mp4", fps, codec)
  # combine_video_audio("res/result.mp4", "tmp.wav", "res/result1.mp4")
  combine_video_audio_ffmpeg("res/tmp.mp4", "tmp.wav", "res/result.mp4")