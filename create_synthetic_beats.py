"""
Keyword: Synthetic data generation
Objective: Given a dataset of percussive single strokes (like https://zenodo.org/records/4327350), stitch them into a beat at a given BPM. Before stitching, perform any processing required like applying fadeout, gain, and normalization.

Inputs:
folder_path: Path to the folder containing single stroke audio files
output_folder (optional): Path to the folder to save synthetic beats
bpm (optional): Tempo in beats per minute
num_beats (optional): Number of synthetic beats to create

Output:
folder with synthetic beats
"""

import os
import random
import argparse
from pydub import AudioSegment

def create_synthetic_beat(folder_path, output_folder, bpm, num_beats):
    interval_duration = (60 / bpm) * 1000  # Convert BPM to milliseconds
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    os.makedirs(output_folder, exist_ok=True)

    for i in range(num_beats):
        selected_files = random.sample(audio_files, 4)
        
        # Before stitching, apply any required processing like fade-out, gain, and normalize
        strokes = [AudioSegment.from_wav(os.path.join(folder_path, file)).fade_out(100).apply_gain(+3).normalize() for file in selected_files]  # Fade out over 100 milliseconds, increase gain by 6 dB, and normalize
        
        # Create a silent audio segment for the total duration of the beat sequence
        total_duration = int(interval_duration * (len(strokes) - 1) + max(len(stroke) for stroke in strokes))
        synthetic_beat = AudioSegment.silent(duration=total_duration)
        
        # Stitch strokes together by placing each stroke at the correct interval
        for idx, stroke in enumerate(strokes):
            position = int(idx * interval_duration)
            synthetic_beat = synthetic_beat.overlay(stroke, position=position)
        
        # Export
        output_file = os.path.join(output_folder, f'synthetic_beat_{i+1}.wav')
        synthetic_beat.export(output_file, format="wav")

    print(f"{num_beats} synthetic beats have been created in '{output_folder}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a synthetic dataset of tabla beats from single strokes.")
    parser.add_argument('--folder_path', nargs='?', default='.', help="Path to the folder containing single stroke audio files (default: current folder)")
    parser.add_argument('--output_folder', type=str, default='synthetic_beats', help="Path to the folder to save synthetic beats (default: synthetic_beats)")
    parser.add_argument('--bpm', type=int, default=60, help="Tempo in beats per minute (default: 60 BPM)")
    parser.add_argument('--num_beats', type=int, default=50, help="Number of synthetic beats to create (default: 50)")

    args = parser.parse_args()

    create_synthetic_beat(args.folder_path, args.output_folder, args.bpm, args.num_beats)

