#!/bin/bash
# Update BPM and KEY metadata for all folders

MUSIC_DIR="/mnt/c/Users/danie/Music/RekordboxDownloads"

echo "=========================================="
echo "  Actualizando BPM y KEY para todas las carpetas"
echo "=========================================="

source venv/bin/activate

# Process Martin Garrix folder
echo ""
python update_metadata.py "$MUSIC_DIR/Martin Garrix"

# Process Lost Frequencies folder
echo ""
python update_metadata.py "$MUSIC_DIR/Lost Frequencies"

# Process HOUSE folder (skip POP for now as it's downloading)
echo ""
python update_metadata.py "$MUSIC_DIR/HOUSE"

echo ""
echo "=========================================="
echo "  ¡Actualización completada!"
echo "=========================================="
