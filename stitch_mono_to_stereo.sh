#!/bin/bash

# Function to process each pair of files
process_files() {
    local left_file="$1"
    local right_file="$2"
    local output_file="$3"

    ffmpeg -i "$left_file" -i "$right_file" -filter_complex "[0:a][1:a]amerge=inputs=2,pan=stereo|c0<c0|c1<c1" -ac 2 "$output_file"
}

# Function to recursively find and process files
stitch_files_recursive() {
    local base_dir="$1"

    # Remove existing stereo files
    find "$base_dir" -type f -name '*stereo*.wav' -exec rm -f {} +

    find "$base_dir" -type d | while read -r dir; do
        # Find left and right files in the current directory
        left_files=($(find "$dir" -maxdepth 1 -type f -name '*left*.wav'))
        right_files=($(find "$dir" -maxdepth 1 -type f -name '*right*.wav'))

        # Ensure that the number of left and right files match
        if [ ${#left_files[@]} -ne ${#right_files[@]} ]; then
            echo "Mismatch in number of left and right files in directory $dir"
            continue
        fi

        for i in "${!left_files[@]}"; do
            left_file="${left_files[$i]}"
            right_file="${right_files[$i]}"
            base_name=$(basename "$left_file")
            base_name=${base_name%left*.wav}
            base_name=${base_name%right*.wav}
            output_file="$dir/${base_name}stereo.wav"
            process_files "$left_file" "$right_file" "$output_file"
        done
    done
}

# Check if a directory is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Call the function with the provided directory
stitch_files_recursive "$1"

echo "All mono files have been stitched into stereo files."
