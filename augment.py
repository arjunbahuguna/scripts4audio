# This script performs parallelized data augmentation
# Step 1: Extract all .wav files into a single 'dataset' folder
# Step 2: Creates separate folders for each augmentation
# Step 3: Augment 'dataset' files and save in corresponding augmentation folder

import os
import librosa
import numpy as np
from shutil import copyfile
from concurrent.futures import ProcessPoolExecutor, as_completed

def create_dataset_folder():
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

def copy_wav_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.wav'):
                src_path = os.path.join(root, file)
                dst_path = os.path.join('dataset', file)
                if os.path.abspath(src_path) != os.path.abspath(dst_path):
                    copyfile(src_path, dst_path)

def time_stretch(y, sr, rate=1.1):
    return librosa.effects.time_stretch(y, rate=rate)

def pitch_shift(y, sr, n_steps=2):
    return librosa.effects.pitch_shift(y, sr, n_steps=n_steps)

def add_noise(y, noise_level=0.002):
    noise = np.random.randn(len(y))
    return y + noise_level * noise

def change_volume(y, gain=1.2):
    return y * gain

def save_augmented_file(y, sr, save_dir, file_name):
    os.makedirs(save_dir, exist_ok=True)
    librosa.output.write_wav(os.path.join(save_dir, file_name), y, sr)

def augment_file(file):
    file_path = os.path.join('dataset', file)
    y, sr = librosa.load(file_path, sr=None)
    
    base_name, ext = os.path.splitext(file)
    
    # Time Stretch
    y_stretched = time_stretch(y, sr, rate=1.1)
    save_augmented_file(y_stretched, sr, 'dataset_time_stretch', f'{base_name}_time_stretch{ext}')

    # Pitch Shift
    y_shifted = pitch_shift(y, sr, n_steps=2)
    save_augmented_file(y_shifted, sr, 'dataset_pitch_shift', f'{base_name}_pitch_shift{ext}')

    # Add Noise
    y_noisy = add_noise(y, noise_level=0.002)
    save_augmented_file(y_noisy, sr, 'dataset_add_noise', f'{base_name}_add_noise{ext}')

    # Change Volume
    y_louder = change_volume(y, gain=1.2)
    save_augmented_file(y_louder, sr, 'dataset_change_volume', f'{base_name}_change_volume{ext}')

def augment_files():
    files = [f for f in os.listdir('dataset') if f.endswith('.wav')]
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(augment_file, file) for file in files]
        for future in as_completed(futures):
            future.result()  # Raise any exceptions that occurred

if __name__ == '__main__':
    create_dataset_folder()
    copy_wav_files()
    augment_files()
