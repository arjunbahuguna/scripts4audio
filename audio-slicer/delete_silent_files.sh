#!/bin/bash

# Path to the text file containing the list of files to delete
file_list="silent_files.txt"

# Check if the file list exists
if [[ ! -f "$file_list" ]]; then
    echo "The file $file_list does not exist."
    exit 1
fi

# Read each line from the file list and delete the file
while IFS= read -r file_path; do
    if [[ -f "$file_path" ]]; then
        rm "$file_path"
        echo "Deleted: $file_path"
    else
        echo "File not found: $file_path"
    fi
done < "$file_list"
