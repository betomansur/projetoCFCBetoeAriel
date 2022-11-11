from playsound import playsound
import numpy as np
from scipy.signal import butter, lfilter, freqz
from matplotlib import pyplot as plt

som = playsound("audio.wav")

def low_pass_filter(adata: np.ndarray, bandlimit: int = 2200, sampling_rate: int = 44100) -> np.ndarray:
        # translate bandlimit from Hz to dataindex according to sampling rate and data size
        bandlimit_index = int(bandlimit * adata.size / sampling_rate)
    
        fsig = np.fft.fft(adata)
        
        for i in range(bandlimit_index + 1, len(fsig)):
            fsig[i] = 0
            
        adata_filtered = np.fft.ifft(fsig)
    
        return np.real(adata_filtered)

