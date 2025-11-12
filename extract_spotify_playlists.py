#!/usr/bin/env python3
"""
Extrae playlists específicas del JSON de Spotify backup
"""

import json
import sys

def extract_playlists(json_file, playlist_names, output_file="spotify_extracted.txt"):
    """Extrae canciones de playlists específicas"""

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_tracks = []
    stats = {}

    for playlist in data.get('playlists', []):
        playlist_name = playlist.get('name', '')

        # Verificar si esta playlist está en la lista deseada
        if playlist_name in playlist_names:
            tracks = playlist.get('tracks', [])
            stats[playlist_name] = len(tracks)

            print(f"📂 {playlist_name}: {len(tracks)} canciones")

            for track in tracks:
                artist = track.get('artist', '')
                title = track.get('track', '')

                if artist and title:
                    # Crear formato "Artista - Canción"
                    track_str = f"{artist} - {title}"

                    # Evitar duplicados
                    if track_str not in all_tracks:
                        all_tracks.append(track_str)

    # Guardar en archivo TXT
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Playlists de Spotify: {', '.join(playlist_names)}\n")
        f.write(f"# Total de canciones: {len(all_tracks)}\n\n")

        for track in all_tracks:
            f.write(f"{track}\n")

    return all_tracks, stats, output_file


if __name__ == "__main__":
    json_file = "lagowski777@2025_11_12.json"

    if not json_file:
        print("Uso: python extract_spotify_playlists.py")
        sys.exit(1)

    # Playlists a extraer
    playlists = ["HOUSE", "POP"]

    print(f"{'='*60}")
    print(f"  Extrayendo playlists de Spotify")
    print(f"{'='*60}\n")

    tracks, stats, output_file = extract_playlists(json_file, playlists)

    print(f"\n{'='*60}")
    print(f"  Resumen")
    print(f"{'='*60}")

    for playlist_name, count in stats.items():
        print(f"  {playlist_name}: {count} canciones")

    print(f"\n  Total único: {len(tracks)} canciones")
    print(f"  Archivo generado: {output_file}")

    print(f"\n{'='*60}")
    print(f"  Primeras 10 canciones:")
    print(f"{'='*60}")

    for i, track in enumerate(tracks[:10], 1):
        print(f"  {i}. {track}")

    if len(tracks) > 10:
        print(f"  ... y {len(tracks) - 10} más")

    print(f"\n💡 Para descargar: ./download.sh {output_file}")
