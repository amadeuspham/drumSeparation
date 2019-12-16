# Drum Separation
An Python implementation of drum separation from music signals. The implementation is based on [Nobutaka Dno, Kenichi Miyamoto, Jonathan Le Roux, Hirokazu Kameoka, and Shigeki Sagayama “Separation of a monaural audio signal into harmonic/percussive components by complementary diffusion on spectrogram”](http://www.cs.tut.fi/~sgn14006/PDF/Ono2008EUSIPCO08.pdf).

This project is the coursework assignment of the course SGN-14007 2019-2020 Introduction to Audio Processing, Tampere University. The audio test samples are provided by the course.

## Table of Contents
- [Repository structure](#repository-structured)
- [Getting started](#getting-started)
  - [Install dependencies](#install-dependencies)
- [Usage](#usage)
  - [Recommended use](#recommended-use)
  - [Results](#results)
- [Testing](#testing)
- [License](#license)
- [Keywords](#keywords)

## Repository structure
```
.
├── output                  --> contains the drum-separated results
├── plots                   --> contains some plots (power spectra and 
				signal-to-noise ratio plots)
├── test_samples            --> contains music audio samples for testing
│   ├── police03short.wav   --> mainly contains drums and pitched instruments
│   │                           with little singing at the end
│   └── project_test1.wav   --> contains singing, pitch-varying instruments and
│				some drums               
├── LICENSE                
├── README.md               
├── Separator.py            --> script to separate a music .wav file to percussion-
│				only (drums) and harmonic-only (singing & others)          
├── testPerformance.py      --> script to test the separation quality with different
│				parameters

```

## Getting started
```bash
git clone https://github.com/amadeuspham/drumSeparation.git
cd drumSeparation
```

### Install dependencies
Make sure you have the following [Python](https://www.python.org) packages installed: [NumPy](https://numpy.org), [Matplotlib](https://matplotlib.org), [LibROSA](https://librosa.github.io/librosa/). You can install all of them through pip by running the following command using on command line:
```bash
pip install numpy matplotlib librosa
```

## Usage
```bash
python Separator.py PATH-TO-MUSIC-WAV-FILE
```

For example:
```bash
python Separator.py test_samples/police03short.wav
```

The separated results will be written to folder /output, in two files: H.wav and P.wav. H.wav contains the harmnonic components of the music file, while P.wav contains the percussive components (drums).

In addition, spectrograms of the original audio file and the separated files are also drawn. Make sure that both H.wav and P.wav are still inside the ./output folder for this to be done.

### Recommended use
Due to the nature of the algorithm, which classifies continuity along y-axis in the spectrogram (frequency) as percussions, and continuity along x-axis in the spectrogram (time) as harmonics, it is recommended to only apply this algorithm on music files with little singing or pitch-varying instruments. THe algorithm works well for drums and pitched instruments tracks.

### Results
Below is the power spectrum of test_samples/police03short.wav
<p align="middle">
	<img src="https://github.com/amadeuspham/drumSeparation/blob/master/plots/police%20spec.png?raw=true" width="800" />
</p>

And the two graphs below are the power spectra of harmonic-only and percussion-only audio outputs, respectively.
<p align="middle">
	<img src="https://github.com/amadeuspham/drumSeparation/blob/master/plots/police%20H%20spec.png?raw=true" width="800" />
	<img src="https://github.com/amadeuspham/drumSeparation/blob/master/plots/police%20P%20spec.png?raw=true" width="800" />
</p>

Comparing these spectrograms to each other, we can clearly see the harmonics (horizontal lines) in the upper spectrogram as well as the percussions (straight, vertical lines) in the lower one. This indicates a very positive performance of the algorithm on this audio sample.

## Testing
You can test the performance of the algorithm with different range compression values (y) or different number of parameters. The default test values are 0, 0.25, 0.5, 0.75 and 1 for y and 5, 10, 20, 60, 100 for the number of iterations.
```bash
python testPerformance.py PATH-TO-MUSIC-WAV-FILE
```

For example:
```bash
python testPerformance.py test_samples/police03short.wav
```

To experiment with your own different values of y and no. iterations, open testPerformance.py, go to the last 2 lines, and add your values as a Python list or NumPy array as the second parameter of each function. Please note that 0 < y <= 1.

## License
Licensed under [MIT](https://github.com/amadeuspham/drumSeparation/blob/master/LICENSE)

## Keywords
python, audio processing, music processing, drum separation, spectrogram