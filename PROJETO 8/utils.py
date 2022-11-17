import numpy as np
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal


def generateSin(freq, amplitude, time, fs):
    n = time*fs
    x = np.linspace(0.0, time, n)
    s = amplitude*np.sin(freq*x*2*np.pi)
    return (x, s)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fft(signal)
    return(xf, yf[0:N//2])

def plotFFT( signal, fs):
    plt.figure()
    x,y = calcFFT(signal, fs)
    plt.plot(x, np.abs(y))
    plt.xticks(np.arange(min(x), max(x)+1, 2500))
    plt.title('Fourier')
    plt.show()


def LPF(signal, cutoff_hz, fs,title = None):
    from scipy import signal as sg
    #####################
    # Filtro
    #####################
    # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
    nyq_rate = fs/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = sg.kaiserord(ripple_db, width)
    taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    return( sg.lfilter(taps, 1.0, signal))