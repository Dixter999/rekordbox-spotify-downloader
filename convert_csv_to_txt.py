#!/usr/bin/env python3
"""
Convert Exportify CSV files to song list txt format.
Input: CSV from https://exportify.net/
Output: txt file with "Artist - Song" format
"""

import csv
import sys
from pathlib import Path


def convert_csv_to_txt(csv_path, output_path=None):
    """Convert Exportify CSV to Artist - Song txt format."""
    csv_path = Path(csv_path)

    if output_path is None:
        output_path = csv_path.with_suffix('.txt')
    else:
        output_path = Path(output_path)

    songs = []

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Get artist and track name
            artist = row.get('Artist Name(s)', '').strip()
            track = row.get('Track Name', '').strip()

            if artist and track:
                # Handle multiple artists (separated by ;)
                # Take only the first/main artist for cleaner search
                main_artist = artist.split(';')[0].strip()
                songs.append(f"{main_artist} - {track}")

    # Remove duplicates while preserving order
    seen = set()
    unique_songs = []
    for song in songs:
        if song.lower() not in seen:
            seen.add(song.lower())
            unique_songs.append(song)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Converted from {csv_path.name}\n")
        f.write(f"# Total songs: {len(unique_songs)}\n\n")
        for song in unique_songs:
            f.write(f"{song}\n")

    print(f"Converted {csv_path.name} -> {output_path.name}")
    print(f"  Total songs: {len(unique_songs)} (removed {len(songs) - len(unique_songs)} duplicates)")

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_csv_to_txt.py <input.csv> [output.txt]")
        print("\nConverts Exportify CSV to 'Artist - Song' format")
        print("Get CSV from: https://exportify.net/")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    convert_csv_to_txt(csv_path, output_path)


if __name__ == "__main__":
    main()
