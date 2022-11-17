import numpy as np
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal

from utils import *

def main():
    fs = 44100
    sd.default.samplerate = fs
    sd.default.channels = 1
    audioModulado, samplerate = sf.read('audioModulado.wav')
    samplesAudio = len(audioModulado)
    t = np.linspace(0,samplesAudio/fs,samplesAudio)
    carrier = np.sin(2*np.pi*14000*t)
    audioDemodulado = audioModulado*carrier
    audioFiltrado = LPF(audioDemodulado,2200,fs)
    
    sd.play(audioFiltrado)
    sd.wait()

    plt.plot(audioDemodulado,t)
    plt.show()

    plotFFT(audioDemodulado,fs)

    plotFFT(audioFiltrado,fs)





if __name__ == "__main__":
	main()