import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
from pathlib import Path

def _decode_wav(path_to_audio : Path):
    fs, x = scipy.io.wavfile.read(path_to_audio)
    k = np.arange(x[:, ...].size)
    return x[:, ...], k/fs

def plot_audio(path_to_audio: Path, path_to_output: Path):
    plt.figure(figsize=[8, 4])
    
    xs, ts = _decode_wav(path_to_audio)
    plt.plot(ts, xs)

    plt.grid()
    plt.title('WAV Signal')
    plt.xlabel("$t$, c")
    plt.ylabel("$Amplitude$")
    plt.tight_layout()
    plt.savefig(path_to_output)

def plot_audio_diff(lhs: Path, rhs: Path, path_to_output: Path):
    plt.figure(figsize=[8, 4])

    plt.subplot(1, 2, 1)

    l_xs, l_ts = _decode_wav(lhs)
    plt.plot(l_ts, l_xs, label='First WAV file')
    
    r_xs, r_ts = _decode_wav(rhs)
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
    
    plt.savefig(path_to_output)
