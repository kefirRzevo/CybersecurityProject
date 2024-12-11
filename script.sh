rm -rf out/*
rm -rf out1/*
mkdir out

ffmpeg -i data/video.mov out/audio.wav
ffmpeg -i data/video.mov out/pic%03d.tiff
ffmpeg -framerate 15 -i out/pic%03d.tiff -i out/audio.wav -c:v ffv1 out/video.mov

ffmpeg -i out/video.mov out1/audio.wav
ffmpeg -i out/video.mov out1/pic%03d.tiff

echo "audio"
diff out/audio.wav out1/audio.wav

echo "pic"
diff out/pic001.tiff out1/pic001.tiff
