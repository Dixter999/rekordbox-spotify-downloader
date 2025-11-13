#!/usr/bin/env python3
"""
Extrae canciones de HOUSE y POP usando Spotify API
"""

import json
import requests
import sys
import os


def get_track_info(track_ids, token):
    """Obtiene información de múltiples tracks"""
    url = "https://api.spotify.com/v1/tracks"
    headers = {"Authorization": f"Bearer {token}"}

    all_tracks = []
    # Spotify permite max 50 tracks por request
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        params = {"ids": ",".join(batch)}

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                for track in data.get('tracks', []):
                    if track:
                        artists = ", ".join([a['name'] for a in track.get('artists', [])])
                        title = track.get('name', '')
                        all_tracks.append(f"{artists} - {title}")
            else:
                print(f"Error API: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    return all_tracks


def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("Uso: python extract_house_pop.py <spotify_backup.json>")
        print("\nEjemplo:")
        print("  python extract_house_pop.py youremail@2025_11_13.json")
        sys.exit(1)

    json_file = sys.argv[1]

    print("="*60)
    print("  Extrayendo HOUSE y POP de Spotify")
    print("="*60)

    # Read Spotify token from environment variable (safer than hardcoding)
    spotify_token = os.getenv('SPOTIFY_TOKEN')
    if not spotify_token:
        print("\n⚠️  ERROR: SPOTIFY_TOKEN no encontrado")
        print("Configure la variable de entorno:")
        print("  export SPOTIFY_TOKEN='your_token_here'")
        sys.exit(1)

    # Leer JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    playlists = data.get('playlists', {})

    all_tracks = []
    stats = {}

    for name in ['HOUSE', 'POP']:
        if name in playlists:
            playlist_data = playlists[name]
            tracks = playlist_data.get('tracks', [])
            track_ids = [t['id'] for t in tracks if 'id' in t]

            print(f"\n📂 {name}: {len(track_ids)} canciones")
            print(f"   Obteniendo información de Spotify...")

            track_names = get_track_info(track_ids, spotify_token)
            stats[name] = len(track_names)

            # Evitar duplicados
            for track in track_names:
                if track not in all_tracks:
                    all_tracks.append(track)

            print(f"   ✓ {len(track_names)} tracks obtenidos")

    # Guardar
    output_file = "spotify_house_pop.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Playlists: HOUSE y POP\n")
        f.write(f"# Total de canciones únicas: {len(all_tracks)}\n\n")
        for track in all_tracks:
            f.write(f"{track}\n")

    print(f"\n{'='*60}")
    print(f"  Resumen")
    print(f"{'='*60}")
    for name, count in stats.items():
        print(f"  {name}: {count} canciones")
    print(f"\n  Total único: {len(all_tracks)} canciones")
    print(f"  Archivo: {output_file}")

    print(f"\n⚠️  ADVERTENCIA:")
    print(f"  ¡Son {len(all_tracks)} canciones!")
    print(f"  La descarga completa puede tomar varias horas.")
    print(f"\n💡 Para descargar: ./download.sh {output_file}")


if __name__ == "__main__":
    main()
