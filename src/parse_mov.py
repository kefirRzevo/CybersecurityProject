import ffmpeg
import cv2
import numpy as np
from pathlib import Path
from logger import logger

repo_path = Path(__file__).parent.parent
counter = 0

def get_free_dir() -> Path:
    global counter
    counter += 1
    path = repo_path / f"out{counter}"
    if not path.exists():
        path.mkdir()
    return path

class ParsedVideo:
    def __init__(self):
        self.path_to_dir = get_free_dir()

    path_to_dir: Path
    fps: int
    frames_count: int

    def path_to_audio(self) -> Path:
        return self.path_to_dir / "audio.wav"

    def path_to_frame(self, i: int) -> Path:
        return self.path_to_dir / f"pic{str(i+1).zfill(3)}.png"

    def path_to_frames(self) -> Path:
        return self.path_to_dir / f"pic%03d.png"

class VideoExtracter:
    def _extract_fps(path_to_video: Path) -> int:
        video = cv2.VideoCapture(path_to_video)
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()
        return int(fps)

    def extract(path_to_video: Path) -> ParsedVideo:
        logger.info(f"Started exctracting {path_to_video}")
        parsed = ParsedVideo()
        parsed.fps = VideoExtracter._extract_fps(path_to_video)
        logger.info(f"Extracted {parsed.fps} fps")
        path_to_frames = parsed.path_to_frames()
        input = ffmpeg.input(path_to_video.as_posix())
        output = ffmpeg.output(input, path_to_frames.as_posix())
        ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
        parsed.frames_count = len(list(parsed.path_to_dir.glob('*.png')))
        # for i in range(frames_count):
        #     img = cv2.imread(parsed.path_to_frame(i).as_posix())
        #     parsed.frames.append(cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
        logger.info(f"Extracted {parsed.frames_count} frames")
        path_to_audio = parsed.path_to_audio()
        output = ffmpeg.output(input, path_to_audio.as_posix())
        ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
        logger.info(f"Extracted {path_to_audio} audio")
        logger.info(f"Finished extracting")
        return parsed

class VideoCombiner:
    def combine(path_to_video: Path, parsed: ParsedVideo):
        logger.info(f"Started combining to {path_to_video}")
        input_frames = ffmpeg.input(parsed.path_to_frames().as_posix(), framerate=parsed.fps)
        input_audio = ffmpeg.input(parsed.path_to_audio().as_posix())
        output = ffmpeg.output(
            input_frames,
            input_audio,
            path_to_video.as_posix(),
            vcodec='ffv1',
            acodec='alac',
            preset='veryslow'
        )
        ffmpeg.run(output, capture_stdout=True, capture_stderr=True)
        logger.info(f"Finished extracting")
