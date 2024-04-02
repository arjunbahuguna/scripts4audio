#!/bin/bash

# Step 1: Download dataset (assuming zip format)
# Define the URL of the zip file and the name you want to save it as
zip_url="http://example.com/path/to/your/file.zip"
zip_file="downloaded_file.zip"

echo "Downloading ZIP file..."
curl -o "$zip_file" "$zip_url"

# Check if download was successful
if [ $? -ne 0 ]; then
    echo "Download failed. Please check the URL and your internet connection."
    exit 1
fi

# Step 2: Inflate the ZIP file
# Define the output directory for the extracted files
output_dir="extracted_files"

# Extract the ZIP file
echo "Extracting ZIP file..."
unzip -q "$zip_file" -d "$output_dir"

# Check if the extraction was successful
if [ $? -ne 0 ]; then
    echo "Extraction failed. Please check the ZIP file."
    exit 1
fi

# Step 3: Change directory
# Check if the output directory exists and change into it
if [ -d "$output_dir" ]; then
    cd "$output_dir"
else
    echo "The extraction directory does not exist."
    exit 1
fi

# You are now in the directory with the extracted files
# Here you would run your processing script
echo "Running the processing script..."
# Add your script's commands or invoke your script here
# ./your_script.sh

# Since you mentioned running the script above,
# Make sure it is executable and located in the correct path
