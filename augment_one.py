# This script performs data augmentation. It extends 'augment.py' with more transformations and removes parallelization.
# This script is best suited for created test augmentations for checking which augmentations sound good on your dataset.
# While 'augment.py' is suited for actually augmenting large datasets.

import os
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from scipy.signal import butter, lfilter

def create_dataset_folder(parent_folder):
    dataset_folder = os.path.join(parent_folder, 'dataset')
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)
    return dataset_folder

def time_stretch(y, rate=1.1):
    return librosa.effects.time_stretch(y, rate=rate)

def pitch_shift(y, sr=48000, n_steps=2):
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

def add_noise(y, noise_level=0.002):
    noise = np.random.randn(len(y))
    return y + noise_level * noise

def compress_dynamic_range(file_path, output_path):
    sound = AudioSegment.from_file(file_path, format="wav")
    compressed_sound = sound.compress_dynamic_range()
    compressed_sound.export(output_path, format="wav")
    y_compressed, sr_compressed = librosa.load(output_path, sr=48000)
    return y_compressed, sr_compressed

def add_reverb(y):
    return librosa.effects.preemphasis(y, coef=0.97)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data)

def save_augmented_file(y, sr, save_dir, file_name):
    os.makedirs(save_dir, exist_ok=True)
    sf.write(os.path.join(save_dir, file_name), y, sr)

def augment_file(file_path, dataset_folder):
    y, sr = librosa.load(file_path, sr=48000)  # Explicitly set sr to 48000
    
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    
    # Time Stretch
    y_stretched = time_stretch(y, rate=1.1)
    save_augmented_file(y_stretched, sr, dataset_folder, f'{base_name}_time_stretch{ext}')

    # Pitch Shift
    y_shifted = pitch_shift(y, sr=48000, n_steps=2)
    save_augmented_file(y_shifted, sr, dataset_folder, f'{base_name}_pitch_shift{ext}')

    # Add Noise
    y_noisy = add_noise(y, noise_level=0.002)
    save_augmented_file(y_noisy, sr, dataset_folder, f'{base_name}_add_noise{ext}')

    # Compress Dynamic Range
    compressed_file_path = os.path.join(dataset_folder, f'{base_name}_compress_dynamic_range{ext}')
    y_compressed, sr_compressed = compress_dynamic_range(file_path, compressed_file_path)
    save_augmented_file(y_compressed, sr_compressed, dataset_folder, f'{base_name}_compress_dynamic_range{ext}')
    
    # Add Reverb
    y_reverb = add_reverb(y)
    save_augmented_file(y_reverb, sr, dataset_folder, f'{base_name}_add_reverb{ext}')
    
    # Bandpass Filter
    y_bandpass = bandpass_filter(y, 300.0, 3400.0, sr)
    save_augmented_file(y_bandpass, sr, dataset_folder, f'{base_name}_bandpass_filter{ext}')

def main(folder_with_wav):
    parent_folder = os.path.abspath(os.path.join(folder_with_wav, os.pardir))
    dataset_folder = create_dataset_folder(parent_folder)
    
    for file in os.listdir(folder_with_wav):
        if file.endswith('.wav'):
            file_path = os.path.join(folder_with_wav, file)
            augment_file(file_path, dataset_folder)

if __name__ == '__main__':
    folder_with_wav = '/path/to/file'
    main(folder_with_wav)
