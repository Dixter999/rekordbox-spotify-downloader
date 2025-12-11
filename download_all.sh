#!/bin/bash
# Download all playlists with lyrics video preference and KEY/BPM detection
# Usage: ./download_all.sh

set -e

echo "========================================="
echo "  Batch Download with Lyrics Priority"
echo "========================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Function to download and update metadata
download_playlist() {
    local file=$1
    local folder=$2

    echo ""
    echo "========================================="
    echo "Downloading: $folder"
    echo "Source: $file"
    echo "========================================="

    python3 youtube_to_rekordbox_enhanced.py "$file" --folder "$folder"

    echo ""
    echo "Updating KEY/BPM metadata for $folder..."
    python3 update_metadata.py "rekordbox_music/$folder"
}

# Download each playlist
# Uncomment the ones you want to download

# Small playlists (quick)
download_playlist "lostfrequencies_2019.txt" "LostFrequencies 2019"
download_playlist "lostfrequencies_2025.txt" "LostFrequencies 2025"
download_playlist "redrocks_2025.txt" "REDROCKS 2025"

# Medium playlists
download_playlist "reggaeton_2025.txt" "REGGAETON"

# Large playlists (will take hours)
download_playlist "house.txt" "HOUSE"
download_playlist "pop.txt" "POP"
download_playlist "andrea_english.txt" "ENGLISH"
download_playlist "andrea_spanish.txt" "SPANISH"

echo ""
echo "========================================="
echo "  All downloads completed!"
echo "========================================="
echo "Your music is in: rekordbox_music/"
echo "Import into Rekordbox and enjoy!"
