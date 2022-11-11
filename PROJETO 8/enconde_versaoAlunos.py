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
    audio, samplerate = sf.read('audio.wav')
    print(audio)
    yAudio = audio
    samplesAudio = len(yAudio)
    t = np.linspace(0,samplesAudio/fs,samplesAudio)

    carrier = np.sin(2*np.pi*14000*t)
    
    #####################
    # Normaliza audio
    #####################
    audioMax = np.max(np.abs(yAudio))
    yAudioNormalizado = yAudio/audioMax

    plt.figure("tempo")
    plt.plot(yAudioNormalizado)
    plt.grid()
    plt.title('audio normalizado no tempo')

 
    #####################
    # Aplica filtro no sinal
    #####################
    print("nao filtrado")
    sd.play(yAudio)
    sd.wait()
    yFiltrado = ut.LPF(yAudioNormalizado, 2200, samplerate)
    print("filtrado")
    plt.figure("tempo")
    plt.plot(yFiltrado)
    plt.grid()
    plt.title('audio filtrado no tempo')
    plotFFT(yFiltrado,fs)
    plt.show()

    plt.title('audio normalizado no tempo')
    signal = carrier * yFiltrado
    plotFFT(signal,fs)
    
    plt.plot(signal,t)
    plt.show()

    sf.write("audioModulado.wav",signal,fs)
    sd.play(yFiltrado)
    sd.wait()

if __name__ == "__main__":
    main()
