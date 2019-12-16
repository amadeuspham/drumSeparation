import librosa as lb
from librosa.display import specshow
import numpy as np
from Separator import separate
import matplotlib.pyplot as plt 
import sys

def test_different_gammas(filename, y_array = np.linspace(0, 1, 5)):
	"""
	Separate an music sample into percussions (drums) and harmonics for 
	different gamma values.
	Plot the spectrograms for percussions and harmonics for all gamma values,
	as well as the signal-to-noise ratio (SNR) for all gamma values

	@params: filename: string - the name of the audio file
			 y_array: 1D numpy array - containing the gamma values to test
	"""
	plt.figure(figsize=(12, 10))

	i = 1

	audioOG, srOG = lb.load(filename, sr=None)
	sum_squares_OG = np.sum(audioOG**2)
	sum_squares_OG_minus_H_array = np.array([])
	sum_squares_OG_minus_P_array = np.array([])

	for y in y_array:
		separate(filename, y);
		audioH, srH = lb.load('output/H.wav', sr=None)
		audioP, srP = lb.load('output/P.wav', sr=None)

		DH = lb.amplitude_to_db(np.abs(lb.stft(audioH)), ref=np.max)
		DP = lb.amplitude_to_db(np.abs(lb.stft(audioP)), ref=np.max)

		sum_squares_OG_minus_H = np.sum((audioOG - audioH)**2)
		sum_squares_OG_minus_P = np.sum((audioOG - audioP)**2)
		sum_squares_OG_minus_H_array = np.append(sum_squares_OG_minus_H_array, 
												 sum_squares_OG_minus_H)
		sum_squares_OG_minus_P_array = np.append(sum_squares_OG_minus_P_array, 
												 sum_squares_OG_minus_P)

		plt.subplot(5, 2, i)
		specshow(DH, y_axis='linear')
		plt.colorbar(format='%+2.0f dB')
		plt.title('Harmonic power spectrogram with gamma = ' + str(y))

		plt.subplot(5, 2, i+1)
		specshow(DP, y_axis='linear')
		plt.colorbar(format='%+2.0f dB')
		plt.title('Percussive power spectrogram with gamma = ' + str(y))

		i += 2

	#plt.suptitle('Different gamma values, ' + filename)
	plt.tight_layout()
	plt.show()

	signal_to_noise_OG_minus_H = 10*np.log10(sum_squares_OG/sum_squares_OG_minus_H_array)
	signal_to_noise_OG_minus_P = 10*np.log10(sum_squares_OG/sum_squares_OG_minus_P_array)
	plt.plot(y_array, signal_to_noise_OG_minus_H, label='Harmonic')
	plt.plot(y_array, signal_to_noise_OG_minus_P, label='Percussive')
	plt.xlabel('Gamma')
	plt.ylabel('SNR')
	plt.legend() 
	plt.title('Signal-to-noise ratio of harmonic and percussive components from file ' 
			+ filename + ' with different gammas')
	plt.show()

def test_diffent_iterations_num(filename, k_array = [5, 10, 20, 60, 100]):
	"""
	Separate an music sample into percussions (drums) and harmonics in different
	number of iterations.
	Plot the spectrograms for percussions and harmonics for all no. iterations,
	as well as the signal-to-noise ratio (SNR) for all no. iterations,

	@params: filename: string - the name of the audio file
			 k_array: 1D numpy array - containing the no. iterations to test
	"""
	plt.figure(figsize=(12, 10))

	i = 1

	audioOG, srOG = lb.load(filename, sr=None)
	sum_squares_OG = np.sum(audioOG**2)
	sum_squares_OG_minus_H_array = np.array([])
	sum_squares_OG_minus_P_array = np.array([])

	for k in k_array:
		separate(filename, k_max = k);
		audioH, srH = lb.load('output/H.wav', sr=None)
		audioP, srP = lb.load('output/P.wav', sr=None)

		DH = lb.amplitude_to_db(np.abs(lb.stft(audioH)), ref=np.max)
		DP = lb.amplitude_to_db(np.abs(lb.stft(audioP)), ref=np.max)

		sum_squares_OG_minus_H = np.sum((audioOG - audioH)**2)
		sum_squares_OG_minus_P = np.sum((audioOG - audioP)**2)
		sum_squares_OG_minus_H_array = np.append(sum_squares_OG_minus_H_array, 
												 sum_squares_OG_minus_H)
		sum_squares_OG_minus_P_array = np.append(sum_squares_OG_minus_P_array, 
												 sum_squares_OG_minus_P)

		plt.subplot(5, 2, i)
		specshow(DH, y_axis='linear')
		plt.colorbar(format='%+2.0f dB')
		plt.title('Harmonic power spectrogram with ' + str(k) + ' iterations')

		plt.subplot(5, 2, i+1)
		specshow(DP, y_axis='linear')
		plt.colorbar(format='%+2.0f dB')
		plt.title('Percussive power spectrogram with ' + str(k) + ' iterations')

		i += 2

	#plt.suptitle('Different no. iterations, ' + filename)
	plt.tight_layout()
	plt.show()

	signal_to_noise_OG_minus_H = 10*np.log10(sum_squares_OG/sum_squares_OG_minus_H_array)
	signal_to_noise_OG_minus_P = 10*np.log10(sum_squares_OG/sum_squares_OG_minus_P_array)
	plt.plot(k_array, signal_to_noise_OG_minus_H, label='Harmonic')
	plt.plot(k_array, signal_to_noise_OG_minus_P, label='Percussive')
	plt.xlabel('No. iterations')
	plt.ylabel('SNR')
	plt.legend() 
	plt.title('Signal-to-noise ratio of harmonic and percussive components from file ' 
			+ filename + ' with different no.iterations')
	plt.show()

if len(sys.argv) == 1:
    print("Please enter the audio filepath after the .py file")
    exit(0)
else:
    filename = sys.argv[1]
	test_different_gammas(filename)
	test_diffent_iterations_num(filename)