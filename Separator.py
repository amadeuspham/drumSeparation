import numpy as np
import librosa as lb
from scipy.signal import stft
from scipy.signal import istft
import math


def auxiliary(a, H, P):
    H = np.c_[np.zeros((np.size(H, 0),), dtype=float), H, np.zeros((np.size(H, 0),), dtype=float)]
    P = np.r_[[np.zeros((np.size(P, 1),), dtype=float)], P, [np.zeros((np.size(P, 1),), dtype=float)]]

    delta = a*(H[:, :-2] - 2*(H[:, 1:-1]) + H[:, 2:]) - (1 - a)*(P[:-2, :] - 2*(P[1:-1, :]) + P[2:, :])

    return delta

# load the signal
audioIn, sr = lb.load("project_test1.wav")

# perform short-time Fourier transform
F = stft(audioIn, sr)[2]

y = 1

# Calculate power spectrogram
W = np.abs(F)**(2*y)

#set initial values
H = W/2
P = W/2
x = np.zeros((np.size(P, 1),), dtype=float)
k = 0
k_max = 5
a_h = 1
a_p = 1
a = (a_p**2)/(a_h**2 + a_p**2)

zeros_H = np.zeros_like(H)
while k < k_max - 1:
    delta = auxiliary(a, H, P)
    
    #H = min(max(H + delta, zeros_H), W)
    H = H + delta
    H [ H < 0 ] = 0
    np.copyto(H, W, where = H > W)
    
    P = W - H
    k += 1
    


H = np.multiply((H >= P).astype('int'), W)
P = np.multiply((P > H).astype('int'), W)

t_h, x_h = istft(H**(1/2*y) * math.e**(1j*np.angle(F)))
t_p, x_p = istft(P**(1/2*y) * math.e**(1j*np.angle(F)))

lb.output.write_wav("H.wav", x_h, sr, norm=False)
lb.output.write_wav("P.wav", x_p, sr, norm=False)

