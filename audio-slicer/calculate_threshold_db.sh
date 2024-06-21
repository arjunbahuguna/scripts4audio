#!/bin/bash
# Determine the loudness of each audio file
# You can use these dB values to set the silence threshold

WAV_DIR="/home/arjbah/Projects/pitch_innovations/data/RAVE/mridangam-sanidha"

for file in "$WAV_DIR"/*.wav; do
    if [[ -f "$file" ]]; then
        rms=$(sox "$file" -n stat 2>&1 | awk '/RMS     amplitude/ { print $3 }')
        if [[ -n "$rms" && "$rms" != "0" ]]; then
            db=$(echo "20 * l($rms) / l(10)" | bc -l)
            echo "File: $file, RMS: $rms, dB: $db"
        else
            echo "File: $file, RMS: $rms, dB: -inf (silence)"
        fi
    fi
done
