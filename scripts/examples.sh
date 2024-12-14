./src/main.py encode --video data/video.mov --secret data/faust.txt --output tmp/video.mov

./src/main.py plot_picture --picture tmp0/pic001.png --diff tmp1/pic001.png --output tmp/plot_pic_diff.png

./src/main.py plot_audio --audio tmp0/audio.wav --diff tmp1/audio.wav --output tmp/plot_audio_diff.png

./src/main.py plot_video --video data/video.mov --diff tmp/video.mov --output tmp/plot_video_diff.png

./src/main.py decode --video tmp/video.mov --secret tmp/faust.txt
