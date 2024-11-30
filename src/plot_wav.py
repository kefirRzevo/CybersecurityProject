import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
from pathlib import Path

def decode_wav(audio_file : Path):
    fs, x = scipy.io.wavfile.read(audio_file)
    k = np.arange(x[:, ...].size)
    return x[:, ...], k/fs

def generate_entropy_png(audio_file: Path, output: Path):
    plt.figure(figsize=[8, 4])
    
    xs, ts = decode_wav(audio_file)
    plt.plot(ts, xs)

    plt.grid()
    plt.title('WAV Signal')
    plt.xlabel("$t$, c")
    plt.ylabel("$Amplitude$")
    plt.tight_layout()
    plt.savefig(output)

def generate_entropy_diff_png(lhs: Path, rhs: Path, output: Path):
    plt.figure(figsize=[8, 4])

    plt.subplot(1, 2, 1)

    l_xs, l_ts = decode_wav(lhs)
    plt.plot(l_ts, l_xs, label='First WAV file')
    
    r_xs, r_ts = decode_wav(rhs)
    plt.plot(r_ts, r_xs, label='Second WAV file')
    
    plt.grid()
    plt.title('WAV Signals')
    plt.xlabel("$t$, c")
    plt.ylabel("$Amplitude$")
    plt.tight_layout()
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(l_ts, l_xs-r_xs, label='Difference')
    
    plt.grid()
    plt.title('WAV Signals Difference')
    plt.xlabel("$t$, c")
    plt.ylabel("$Amplitude$")
    plt.tight_layout()
    plt.legend()
    
    plt.savefig(output)