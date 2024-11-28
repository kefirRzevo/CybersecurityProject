#!/usr/bin/python3

import argparse
from pathlib import Path
from video_parser import ParsedVideo, VideoExtracter, VideoCombiner
from video_entropy import VideoEntropy

repo_path = Path(__file__).parent.parent

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    encode = subparsers.add_parser("encode")
    encode.add_argument("--video", required=True, help="path to video")
    encode.add_argument("--secret", help="path to secret file")
    encode.add_argument("--output", help="path to output video")

    entropy = subparsers.add_parser("entropy")
    entropy.add_argument("--video", required=True, help="path to video")
    entropy.add_argument("--period", type=int, default=None, help="entropy \"period\". If not specified, feature desabled")
    entropy.add_argument("--output", help="path to result file with entropy representation")
    entropy.add_argument(
        "--diff", 
        help="path to another video. Instead of show entropy of `--video`" 
        "param, show differnce between `path to video` and `path to another video` videos"
    )

    decode = subparsers.add_parser("decode")
    
    args = parser.parse_args()
    print(args)
    match args.command:
        case "entropy":
            path_to_video = Path(args.video)
            entropy_period = int(args.period) if args.period is not None else None
            path_to_another = Path(args.diff) if args.diff is not None else None
            video = VideoExtracter.extract(path_to_video)
            path_to_out_video = Path(args.output) if args.output is not None else Path(str(args.video)[:-4] + ("_entropy.mp4" if entropy_period is not None else "_entropy.png"))
            another = VideoExtracter.extract(path_to_another) if path_to_another is not None else None
            entr_calc = VideoEntropy(video.frames)
            entr_calc.entropy_image(
                another.frames if another is not None else None,
                path_to_out_video,
                entropy_period  
            )

        case "encode":
            
            pass
        case "decode":
            
            pass
        case _ :
            print("ERROR")
    
    # path_to_mp4: Path = args.video
    # path_to_secret: Path = args.secret
    # path_to_final_mp4: Path = args.output
    
    # parsed: ParsedVideo = VideoExtracter.extract(path_to_mp4)

    # VideoCombiner.combine(repo_path / "tmp" / "fuck.mp4", parsed)
