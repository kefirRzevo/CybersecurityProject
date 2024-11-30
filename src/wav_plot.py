import matplotlib.pyplot as plt
import scipy.io.wavfile

def decode_wav(audio_file : Path):
    fs, x=scipy.io.wavfile.read(audio_file)
    k=np.arange(x[:80000, ...].size)
    return x[:80000, ...], k/fs

def generate_entropy_png(audio_file: Path, output: Path):
    plt.figure(figsize=[8, 4])
    
    xs, ts = decode_wav(output)
    plt.plot(ts, xs)

    plt.grid()
    plt.xlabel("$t$, c")
    plt.ylabel("$Amplitude$")
    plt.tight_layout()
    plt.savefic(output)

def generate_entropy_diff_png(lhs: Path, rhs: Path, output: Path):
    plt.figure(figsize=[8, 4])
    fig, (ax1, ax2) = plt.subplots(1, 2)

    l_xs, l_ts = decode_wav(lhs)
    ax1.plot(l_ts, l_xs, label='First WAV file')
    
    r_xs, r_ts = decode_wav(rhs)
    ax1.plot(r_ts, r_xs, label='Second WAV file')
    
    ax1.grid()
    ax1.xlabel("$t$, c")
    ax1.ylabel("$Amplitude$")
    ax1.tight_layout()
    ax1.legend()

    ax2.scatter(ts, xs-xs1, label='Difference')
    
    ax2grid()
    ax2.xlabel("$t$, c")
    ax2.ylabel("$Amplitude$")
    ax2.tight_layout()
    ax2.legend()
    
    plt.savefic(output)
