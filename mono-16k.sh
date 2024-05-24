#!/bin/bash
# Not meant for small datasets (<100GB)
# Input: Wav files in current directory and subdirectories
# Output: Wav files coverted to mono and resampled, and log file. 
# Note: Files will be renamed and subdirectory structure will not be preserved, ie. all files will be put in single folder called "out"
# Arguments: at "xargs -P4", you can set 4 to number of CPU cores available on your system

# Log file path and start time
log_file="./processing_log.txt"
start_time=$(date +%s)

# Ensure the output directory and log file exist
mkdir -p ./out
touch "$log_file"

# Preliminary checks for required commands
commands=("sox" "md5sum" "cut" "basename")
for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: Required command '$cmd' is not available." | tee -a "$log_file"
        exit 1
    fi
done

# Calculate total number of files for progress tracking
total_files=$(find . -type f -name '*.wav' ! -path "./out/*" | wc -l)

# Using find and xargs for parallel processing
processed_files=0
find . -type f -name '*.wav' ! -path "./out/*" | xargs -P4 -I{} bash -c '
    file="{}"
    log_file="$1"
    total_files="$2"
    filename=$(basename "$file")
    # Generate a more unique identifier for the output filename
    hash=$(echo "$file" | md5sum | cut -f1 -d" ")
    outfile="./out/${hash}.wav"
    if sox "$file" -c 1 -r 16000 "$outfile"; then
        # Delete the source file after successful processing
        if ! rm "$file" 2>>"$log_file"; then
            echo "Failed to delete $file" >>"$log_file"
        fi
        echo "Processed ${outfile}" >>"$log_file"
    else
        echo "Failed to process $file" >>"$log_file"
    fi
' "$log_file" "$total_files"

# Count processed files for a rough progress estimate
processed_files=$(ls ./out | wc -l)

# Calculate and display script runtime
end_time=$(date +%s)
runtime=$((end_time-start_time))

# Final message and logging
echo "Processed $processed_files out of $total_files files in $runtime seconds." | tee -a "$log_file"
