#!/usr/bin/python3

import cv2
import numpy as np
import scipy.io.wavfile as wv
from pydub import AudioSegment
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip
from logger import logger

repo_path = Path(__file__).parent.parent

class ParsedVideo:
    fps: int
    frames: list[np.ndarray]
    path_to_wav: Path

class VideoExtracter:
    def _extract_fps(video: cv2.VideoCapture) -> int:
        fps = video.get(cv2.CAP_PROP_FPS)
        return int(fps)

    def _extract_frames(video: cv2.VideoCapture) -> list[np.ndarray]:      
        frames: list[np.ndarray] = []
        while True:
            ret, frame = video.read()
            if not ret:
                break
            frames.append(frame)
        return frames

    def _extract_wav_from_mp4(path_to_mp4: Path, path_to_wav: Path):
        audio = AudioSegment.from_file(path_to_mp4, format="mp4")
        audio.export(path_to_wav, format="wav")

    def _get_path_to_wav(path_to_mp4: Path) -> Path:
        path_to_wav = repo_path / "tmp"
        path_to_wav.touch()
        return path_to_wav / f"{path_to_mp4.stem}_audio.wav"

    def extract(path_to_mp4: Path) -> ParsedVideo:
        parsed = ParsedVideo()
        video = cv2.VideoCapture(path_to_mp4)
        if not video.isOpened():
            raise RuntimeError(f"Unable to open video file: {path_to_mp4}")
        parsed.fps = VideoExtracter._extract_fps(video)
        logger.info(f"Extracted {parsed.fps} fps from {path_to_mp4}")
        parsed.frames = VideoExtracter._extract_frames(video)
        logger.info(f"Extracted {len(parsed.frames)} frames from {path_to_mp4}")
        path_to_wav = VideoExtracter._get_path_to_wav(path_to_mp4)
        parsed.path_to_wav = path_to_wav
        VideoExtracter._extract_wav_from_mp4(path_to_mp4, path_to_wav)
        logger.info(f"Extracted {path_to_wav} from {path_to_mp4}")
        video.release()
        return parsed

class VideoCombiner:
    def _get_path_to_raw_mp4(path_to_final_mp4: Path) -> Path:
        path_to_raw_mp4 = repo_path / "tmp"
        path_to_raw_mp4.touch()
        return path_to_raw_mp4 / f"{path_to_final_mp4.stem}_frames.mp4"

    def _combine_to_raw_mp4(path_to_raw_mp4: Path, video: ParsedVideo):
        height, width, _ = video.frames[0].shape
        shape = (width, height)
        fourcc = cv2.VideoWriter.fourcc(*'vp09')
        video_writer = cv2.VideoWriter(path_to_raw_mp4, fourcc, video.fps, shape)
        for frame in video.frames:
            video_writer.write(frame)
        video_writer.release()

    def _combine_to_mp4(path_to_raw_mp4: Path, path_to_final_mp4: Path, video: ParsedVideo):
        video_clip = VideoFileClip(path_to_raw_mp4.as_posix())
        audio_clip = AudioFileClip(video.path_to_wav.as_posix())
        res = video_clip.set_audio(audio_clip)
        res.write_videofile(path_to_final_mp4.as_posix(), logger=None)

    def combine(path_to_final_mp4: Path, video: ParsedVideo):
        path_to_raw_mp4 = VideoCombiner._get_path_to_raw_mp4(path_to_final_mp4)
        logger.info(f"Path to raw mp4 {path_to_raw_mp4}")
        VideoCombiner._combine_to_raw_mp4(path_to_raw_mp4, video)
        logger.info(f"Raw mp4 created at {path_to_raw_mp4}")
        VideoCombiner._combine_to_mp4(path_to_raw_mp4, path_to_final_mp4, video)
        logger.info(f"Combined to {path_to_final_mp4}")
