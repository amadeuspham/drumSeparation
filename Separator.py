import numpy as np
import librosa as lb
#from scipy.signal import stft, istft
import math

def find_delta(a, H, P):
    """
    Find the delta value to update harmonic and percussive power spectrograms
    @ params: a: float - controls the weight of harmonic and percussive components
              H: 2D numpy array - power spectrum of harmonic component
              P: 2D numpy array - power spectrum of percussive component
    """
    H = np.c_[np.zeros((np.size(H, 0),), dtype=float), H, np.zeros((np.size(H, 0),), dtype=float)]
    P = np.r_[[np.zeros((np.size(P, 1),), dtype=float)], P, [np.zeros((np.size(P, 1),), dtype=float)]]

    delta = a*(H[:, :-2] - 2*(H[:, 1:-1]) + H[:, 2:])/4 - (1 - a)*(P[:-2, :] - 2*(P[1:-1, :]) + P[2:, :])/4

    return delta

def separate(filename, y=1, a_h=1, a_p=1, k_max=20):
    """
    Separate an audio file into 2 audio files, one for percussive components (drums)
    and one for harmonic components (singing & others)
    @params: filename: string - input audio file
             y: float (0 < y <= 1) - range compression coefficient, facilitates the separation
             a_h and a_p: float - control the weights of the horizontal and vertical smoothness
             k_max: number of iterations

    @return: 2 audio files "H.wav" and "P.wav" are created, which contain harmonic and
             percussive components, respoectively, and saved into the current directory.
    """
    # load the signal
    audioIn, sr = lb.load(filename, sr=None)

    # perform short-time Fourier transform
    n_fft = 2048
    n_audio = len(audioIn)
    # make sure that the signal length will not be trimmed after stft and istft
    audioIn_pad = lb.util.fix_length(audioIn, n_audio + n_fft // 2)
    F = lb.stft(audioIn_pad, n_fft=n_fft)

    # Calculate a range-compressed version of the power spectrogram
    W = np.abs(F)**(2*y)

    # Set initial values for harmonic and percussive power spectrogram
    H = W/2
    P = W/2
    k = 0
    a = (a_p**2)/(a_h**2 + a_p**2)

    while k < k_max - 1:
        delta = find_delta(a, H, P)
        
        #H = min(max(H + delta, 0), W)
        H = H + delta
        H [ H < 0 ] = 0
        np.copyto(H, W, where = H > W)
        
        P = W - H
        k += 1
        
    # binarize separation output
    H = np.multiply((H >= P).astype('int'), W)
    P = np.multiply((P > H).astype('int'), W)
    # convert separated power spectrums back to waveform signals
    # by inverse short time Fourier transform
    x_h = lb.istft(H**(1/2*y) * math.e**(1j*np.angle(F)), length=n_audio)
    x_p = lb.istft(P**(1/2*y) * math.e**(1j*np.angle(F)), length=n_audio)

    lb.output.write_wav("H.wav", x_h, sr, norm=False)
    lb.output.write_wav("P.wav", x_p, sr, norm=False)

# police = 'police03short.wav'
# project = 'project_test1.wav'
# separate(project)