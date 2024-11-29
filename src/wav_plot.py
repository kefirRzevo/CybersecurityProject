import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
from pathlib import Path

repo_path = Path(__file__).parent.parent

def decode_wav(audio_file):
    fs, x=scipy.io.wavfile.read(audio_file)
    k=np.arange(x[:, ...].size)
    return x[:, ...], k/fs

def plot_wav(audio_file):
    plt.figure(figsize=[8, 4])

    xs, ts = decode_wav(repo_path / 'tmp' / 'parsedplayback.wav')
    plt.plot(ts, xs)

    xs, ts = decode_wav(audio_file)
    plt.plot(ts, xs)

    plt.grid()
    plt.xlabel("$t$, c")
    plt.ylabel("$x[k]$")
    plt.tight_layout()
    plt.show()

plot_wav(repo_path / 'res' / 'videoplayback.wav')
