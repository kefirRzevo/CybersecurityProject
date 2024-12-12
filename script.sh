rm -rf out/*
rm -rf out1/*
mkdir out
mkdir out1

ffmpeg -i data/video.mov out/audio.wav
ffmpeg -i data/video.mov out/pic%03d.png
ffmpeg -framerate 15 -i out/pic%03d.png -i out/audio.wav -c:v ffv1 -c:a alac -preset veryslow out/video.mov 

ffmpeg -i out/video.mov out1/audio.wav
ffmpeg -i out/video.mov out1/pic%03d.png

echo "audio"
diff out/audio.wav out1/audio.wav

echo "pic"
diff out/pic001.png out1/pic001.png
