#!/usr/bin/python3

import argparse
from pathlib import Path
from video_parser import ParsedVideo, VideoExtracter, VideoCombiner
from frame_lsb_steganography import LSBFrameEncode, LSBFrameDecode
from wav_lsb_steganography import LSBWavEncode, LSBWavDecode
from picture_entropy import VideoEntropy

repo_path = Path(__file__).parent.parent

def generate_entropy_png(picture: str, output: str, diff: bool):
    path_to_picture = Path(picture)
    path_to_output = Path(output)

def generate_wav_plot(audio: str, output: str, diff: bool):
    path_to_audio = Path(audio)
    path_to_output = Path(output)

def generate_encoded_video(video: str, secret: str, output: str):
    path_to_video = Path(video)
    path_to_secret = Path(secret)
    path_to_output = Path(output)

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

    entropy = subparsers.add_parser("entropy_png")
    entropy.add_argument("--picture", type=str, required=True, help="path to picture png")
    entropy.add_argument("--output", required=True, help="path to picture entropy plot")
    entropy.add_argument("--diff", default=False, type=bool, action="store_true", help="plot diff between encoded picture and raw")

    plot = subparsers.add_parser("wav_plot")
    plot.add_argument("--audio", required=True, help="path to audio wav")
    plot.add_argument("--output", required=True, help="path to audio plot")
    plot.add_argument("--diff", help="plot diff between encoded audio and raw")

    args = parser.parse_args()
    print(args)
    match args.command:
        case "entropy_png":
            pass
        case "plot_wav":
            pass
        case "encode":
            pass
        case "decode":
            pass
        case _ :
            print("ERROR")
