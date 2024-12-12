#!/usr/bin/python3

import argparse
from pathlib import Path
from parse_mov import ParsedVideo, VideoExtracter, VideoCombiner
from lsb_png_steganography import LSBPngEncode, LSBPngDecode
from lsb_wav_steganography import LSBWavEncode, LSBWavDecode
import plot_picture
import plot_audio

repo_path = Path(__file__).parent.parent

def _split_to_chunks(msg: str, chunks_count: int, frame_max_len: int) -> list[str]:
    chunks = ["" for _ in range(chunks_count)]
    for i in range(chunks_count):
        begin = i * frame_max_len
        end = (i + 1) * frame_max_len
        if end >= len(msg):
            end = len(msg) - 1
            chunks[i] = msg[begin:end]
            break
        chunks[i] = msg[begin:end]
    return chunks

def generate_video_plot(video: str, output: str, diff: str | None):
    path_to_video = Path(video)
    path_to_output = Path(output)

    if diff is None:
        plot_picture.plot_video(path_to_video, path_to_output)
        return

    path_to_diff = Path(diff)
    plot_picture.plot_picture_diff(path_to_video, path_to_diff, path_to_output)

def generate_picture_plot(picture: str, output: str, diff: str | None):
    path_to_picture = Path(picture)
    path_to_output = Path(output)

    if diff is None:
        plot_picture.plot_picture(path_to_picture, path_to_output)
        return

    path_to_diff = Path(diff)
    plot_picture.plot_picture_diff(path_to_picture, path_to_diff, path_to_output)

def generate_audio_plot(audio: str, output: str, diff: str | None):
    path_to_audio = Path(audio)
    path_to_output = Path(output)

    if diff is None:
        plot_audio.plot_audio(path_to_audio, path_to_output)
        return

    path_to_diff = Path(diff)
    plot_audio.plot_audio_diff(path_to_audio, path_to_diff, path_to_output)

def generate_encoded_video(video: str, secret: str, output: str):
    path_to_video = Path(video)
    path_to_secret = Path(secret)
    path_to_output = Path(output)
    with open(path_to_secret) as f:
        msg = f.read()
    parsed: ParsedVideo = VideoExtracter.extract(path_to_video)
    chunks_count = parsed.frames_count
    frame_max_len = LSBPngEncode.encode_max_len(parsed.path_to_frame(0))
    frames_max_len = frame_max_len * chunks_count
    audio_max_len = LSBWavEncode.encode_max_len(parsed.path_to_audio())
    max_len = min(frames_max_len, audio_max_len)
    if len(msg) > max_len:
        raise Exception("too large secret message")

    encoded = ParsedVideo()
    encoded.fps = parsed.fps
    encoded.frames_count = parsed.frames_count

    chunks = _split_to_chunks(msg, chunks_count, frame_max_len)
    for i in range(chunks_count):
        LSBPngEncode.encode(parsed.path_to_frame(i), encoded.path_to_frame(i), chunks[i])

    LSBWavEncode.encode(parsed.path_to_audio(), encoded.path_to_audio(), msg)
    VideoCombiner.combine(path_to_output, encoded)

def generate_decoded_video(video: str, secret: str):
    path_to_video = Path(video)
    path_to_secret = Path(secret)

    parsed: ParsedVideo = VideoExtracter.extract(path_to_video)
    chunks_count = parsed.frames_count

    chunks = ["" for _ in range(chunks_count)]
    for i in range(chunks_count):
        chunks[i] = LSBPngDecode.decode(parsed.path_to_frame(i))

    frame_msg = "".join(chunks)
    audio_msg = LSBWavDecode.decode(parsed.path_to_audio())
    print(audio_msg)
    print(frame_msg)
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

    entropy = subparsers.add_parser("plot_picture")
    entropy.add_argument("--picture", type=str, help="path to picture png")
    entropy.add_argument("--output", required=True, type=str, help="path to picture entropy plot")
    entropy.add_argument("--diff", default=None, type=str, help="path to encoded picture to see the difference")

    entropy = subparsers.add_parser("plot_video")
    entropy.add_argument("--video", type=str, help="path to video mov")
    entropy.add_argument("--output", required=True, type=str, help="path to video entropy plot")
    entropy.add_argument("--diff", default=None, type=str, help="path to encoded video to see the difference")

    plot = subparsers.add_parser("plot_audio")
    plot.add_argument("--audio", required=True, help="path to audio wav")
    plot.add_argument("--output", required=True, help="path to audio plot")
    plot.add_argument("--diff", default=None, type=str, help="path to encoded audio to see the difference")

    args = parser.parse_args()
    print(args)
    match args.command:
        case "plot_video":
            generate_video_plot(args.video, args.output, args.diff)
            pass
        case "plot_picture":
            generate_picture_plot(args.picture, args.output, args.diff)
            pass
        case "plot_audio":
            generate_audio_plot(args.audio, args.output, args.diff)
            pass
        case "encode":
            generate_encoded_video(args.video, args.secret, args.output)
            pass
        case "decode":
            generate_decoded_video(args.video, args.secret)
            pass
        case _ :
            print("ERROR")
