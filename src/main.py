import argparse
from pathlib import Path
from video_parser import ParsedVideo, VideoExtracter, VideoCombiner

repo_path = Path(__file__).parent.parent

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    encode = subparsers.add_parser("encode")
    encode.add_argument("--video", required=True, help="path to video")
    encode.add_argument("--secret", help="path to secret file")
    encode.add_argument("--output", help="path to output video")

    decode = subparsers.add_parser("decode")
    
    args = parser.parse_args()
    print(args)
    
    # path_to_mp4: Path = args.video
    # path_to_secret: Path = args.secret
    # path_to_final_mp4: Path = args.output
    
    # parsed: ParsedVideo = VideoExtracter.extract(path_to_mp4)

    # VideoCombiner.combine(repo_path / "tmp" / "fuck.mp4", parsed)
