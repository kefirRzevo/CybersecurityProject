#!/usr/bin/python3

import cv2
import sys
import numpy as np
import scipy.io.wavfile as wv
from pydub import AudioSegment
from pathlib import Path
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip
import subprocess

repo_path = Path(__file__).parent.parent

class ParsedVideo:
  path_to_mp4: Path
  fps: int
  codec: int
  frames: list[np.ndarray]
  path_to_wav: Path
  audio_fs: float
  audio_data: np.ndarray

class VideoExtracter:
  def extract_fps(video: cv2.VideoCapture) -> int:
      fps = video.get(cv2.CAP_PROP_FPS)
      return int(fps)

  def extract_codec(video: cv2.VideoCapture) -> int:
      codec = video.get(cv2.CAP_PROP_FOURCC)
      return int(codec)

  def extract_frames(video: cv2.VideoCapture) -> list[cv2.typing.MatLike]:      
      frames: list[np.ndarray] = []
      frame_count = 0
      
      while True:
          ret, frame = video.read()
          if not ret:  # No more frames
              break
          frames.append(frame)
          frame_count += 1

      return frames

  def extract_wav_from_mp4(path_to_mp4: Path, path_to_wav: Path):
    audio = AudioSegment.from_file(path_to_mp4, format="mp4")
    audio.export(path_to_wav, format="wav")
    print(f"Extracted {path_to_wav} from {path_to_mp4}")

  def extract(path_to_mp4: Path) -> ParsedVideo:
      parsed = ParsedVideo()
      parsed.path_to_mp4 = path_to_mp4
      video = cv2.VideoCapture(path_to_mp4)
      if not video.isOpened():
          raise ValueError(f"Unable to open video file: {path_to_mp4}")
      parsed.fps = VideoExtracter.extract_fps(video)
      print(f"Extracted {parsed.fps} fps from {path_to_mp4}")
      parsed.codec = VideoExtracter.extract_fps(video)
      print(f"Extracted {parsed.codec} codec from {path_to_mp4}")
      parsed.frames = VideoExtracter.extract_frames(video)
      print(f"Extracted {len(parsed.frames)} frames from {path_to_mp4}")
      path_to_wav = repo_path / "res" / "extracted_audio.wav"
      parsed.path_to_wav = path_to_wav
      VideoExtracter.extract_wav_from_mp4(path_to_mp4, path_to_wav)
      parsed.audio_fs, parsed.audio_data = wv.read(path_to_wav)
      print(f"Extracted {parsed.audio_fs} from {path_to_wav}")
      video.release()

class VideoCombiner:
   def combine(path_to_combined_mp4: Path, video: ParsedVideo):
      pass

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
  
  parsed = VideoExtracter.extract(sys.argv[1])
  # frames, fps, codec = extract_frames(sys.argv[1])

  # print(frames[0].shape)
  # print(fps)
  # extract_audio_with_pydub(sys.argv[1], "tmp.wav")
  # fs, x = wv.read("tmp.wav")
  # print(x.shape)


  # # assembling frame array and wav audio array

  # create_video_from_frames(frames, "res/tmp.mp4", fps, codec)
  # # combine_video_audio("res/result.mp4", "tmp.wav", "res/result1.mp4")
  # combine_video_audio_ffmpeg("res/tmp.mp4", "tmp.wav", "res/result.mp4")