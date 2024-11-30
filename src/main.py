#!/usr/bin/python3

import argparse
import numpy as np
from pathlib import Path
from video_parser import ParsedVideo, VideoExtracter, VideoCombiner
from lsb_frame_steganography import LSBFrameEncode, LSBFrameDecode
from lsb_wav_steganography import LSBWavEncode, LSBWavDecode
from plot_picture import PictureEntropy
import plot_wav

repo_path = Path(__file__).parent.parent

def generate_entropy_png(picture: str, output: str, diff: str | None, period: int | None):
    PictureEntropy.png_entropy_image(picture, diff, output, period)

def generate_entropy_video(video_path: str, output: str, diff: str | None):
    video = VideoExtracter.extract(Path(video_path))
    video_entr = PictureEntropy(video.frames, video.fps)

    another = None 
    if diff is not None:
        another_video = VideoExtracter.extract(Path(diff))
        another = another_video.frames

    video_entr.entropy_image(another, Path(output), None)

def generate_wav_plot(audio: str, output: str, diff: str | None):
    path_to_audio = Path(audio)
    path_to_output = Path(output)

    if diff is None:
        plot_wav.generate_entropy_png(path_to_audio, path_to_output)
        return

    path_to_diff = Path(diff)

    plot_wav.generate_entropy_diff_png(path_to_audio, path_to_diff, path_to_output)

def generate_encoded_video(video: str, secret: str, output: str):
    path_to_video = Path(video)
    path_to_secret = Path(secret)
    path_to_output = Path(output)
    with open(path_to_secret) as f:
        msg = f.read()
    parsed_video: ParsedVideo = VideoExtracter.extract(path_to_video)
    chunks_count = len(parsed_video.frames)
    frame_max_len = LSBFrameEncode.encode_max_len(parsed_video.frames[0])
    frames_max_len = frame_max_len * len(parsed_video.frames)
    audio_max_len = LSBWavEncode.encode_max_len(parsed_video.path_to_wav)
    max_len = min(frames_max_len, audio_max_len)
    if len(msg) > max_len:
        raise Exception("too large secret message")
    
    is_end = False
    chunks = ["" for i in range(0, chunks_count * frame_max_len, frame_max_len)]
    for i in range(chunks_count):
        begin = i
        end = i + frame_max_len
        if len(msg) >= end:
            end = len(msg)
            is_end = True
        if is_end:
            break
        chunks[i] = msg[begin:end]

    copied = np.copy(parsed_video)

    for i in range(chunks_count):
        if chunks[i] != "":
            parsed_video.frames[i] = LSBFrameEncode.encode(parsed_video.frames[i], chunks[i])
    encoded_wav = repo_path / "tmp" / "encoded_audio.wav"
    LSBWavEncode.encode(copy.path_to_wav, encoded_wav, msg)
    VideoCombiner.combine(path_to_output, parsed_video)

def generate_decoded_video(video: str, secret: str):
    path_to_video = Path(video)
    path_to_secret = Path(secret)

    parsed_video: ParsedVideo = VideoExtracter.extract(path_to_video)
    chunks_count = len(parsed_video.frames)
    
    is_end = False
    chunks = ["" for _ in range(chunks_count)]
    for i in range(chunks_count):
        if is_end:
            break
        chunks[i] = LSBFrameDecode.decode(parsed_video.frames[i])
        if chunks[i] == "":
            is_end = True

    frame_msg = "".join(chunks)
    print(parsed_video.path_to_wav.as_posix())
    audio_msg = LSBWavDecode.decode(parsed_video.path_to_wav)
    audio_msg = LSBWavDecode.decode(Path("./tmp/encoded_audio.wav"))
    print(audio_msg)
    with open(path_to_secret, "w") as f:
        f.write(audio_msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    encode = subparsers.add_parser("encode")
    encode.add_argument("--video", type=str, required=True, help="path to video")
    encode.add_argument("--secret", type=str, required=True, help="path to secret file")
    encode.add_argument("--output", type=str, required=True, help="path to output video")

    decode = subparsers.add_parser("decode")
    decode.add_argument("--video", type=str, required=True, help="path to video")
    decode.add_argument("--secret", type=str, required=True, help="path to secret file")
    decode.add_argument("--output", type=str, required=True, help="path to output video")

    entropy = subparsers.add_parser("entropy")
    entropy.add_argument("--picture", type=str, help="path to picture png")
    entropy.add_argument("--video", type=str, help="path to video mp4")
    entropy.add_argument("--output", required=True, help="path to picture entropy plot")
    entropy.add_argument("--diff", default=None, type=str, help="path to encoded picture or video to see difference")
    entropy.add_argument("--period", default=None, type=int)

    plot = subparsers.add_parser("wav_plot")
    plot.add_argument("--audio", required=True, help="path to audio wav")
    plot.add_argument("--output", required=True, help="path to audio plot")
    plot.add_argument("--diff", default=None, type=str, help="path to encoded audio to see diff")

    args = parser.parse_args()
    print(args)
    match args.command:
        case "entropy":
            if args.picture is not None:
                generate_entropy_png(args.picture, args.output, args.diff, args.period)
            elif args.video is not None:
                generate_entropy_video(args.video, args.output, args.diff)
            else:
                parser.error("for command `entorpy` --video or --picture must be specified")
            
        case "wav_plot":
            generate_wav_plot(args.audio, args.output, args.diff)
            pass
        case "encode":
            generate_encoded_video(args.video, args.secret, args.output)
            pass
        case "decode":
            pass
        case _ :
            print("ERROR")
