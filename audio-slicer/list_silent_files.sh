#!/bin/bash

# Directory containing the audio files
DIRECTORY="path/to/audio/files"

# Output file
OUTPUT_FILE="silent_files.txt"

# Initialize the output file
> "$OUTPUT_FILE"

# Loop through each file in the directory
for FILE in "$DIRECTORY"/*; do
  # Check if the file is an audio file (you can add more extensions if needed)
  if [[ "$FILE" == *.mp3 || "$FILE" == *.wav || "$FILE" == *.flac ]]; then
    # Get the mean volume of the file
    MEAN_VOLUME=$(ffmpeg -i "$FILE" -af "volumedetect" -f null /dev/null 2>&1 | grep 'mean_volume' | awk '{print $5}')

    # If the mean volume is less than or equal to -40 dB, consider it as silent
    if (( $(echo "$MEAN_VOLUME <= -40" | bc -l) )); then
      # Remove any double slashes from the file path
      FILE=$(echo "$FILE" | sed 's|//|/|g')
      echo "$FILE" >> "$OUTPUT_FILE"
    fi
  fi
done

echo "Completely silent files have been listed in $OUTPUT_FILE"
