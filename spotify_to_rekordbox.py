#!/usr/bin/env python3
"""
Spotify to Rekordbox - Pipeline completo
Extrae playlist de Spotify y descarga automáticamente en Rekordbox
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path


def extract_playlist_id(url):
    """Extrae el ID de playlist de una URL de Spotify"""
    match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None


def get_spotify_tracks(playlist_url):
    """Usa spotify-backup para extraer tracks de una playlist"""
    print(f"🎵 Extrayendo tracks de Spotify...")
    print(f"URL: {playlist_url}\n")

    try:
        # Ejecutar spotify-backup
        result = subprocess.run(
            ["python3", "spotify-backup/spotify-backup.py", playlist_url],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"Error ejecutando spotify-backup: {result.stderr}")
            return []

        # Parsear el output JSON
        output_file = "spotify-backup/playlists.json"
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extraer tracks
            tracks = []
            for playlist in data.get('playlists', []):
                for track in playlist.get('tracks', []):
                    artist = track.get('artist', '')
                    title = track.get('track', '')
                    if artist and title:
                        tracks.append(f"{artist} - {title}")

            return tracks

        print("No se encontró archivo de salida de spotify-backup")
        return []

    except subprocess.TimeoutExpired:
        print("Timeout esperando respuesta de Spotify")
        return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []


def create_download_list(tracks, output_file="spotify_playlist.txt"):
    """Crea archivo de texto con la lista de tracks"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Playlist de Spotify - {len(tracks)} canciones\n")
        f.write(f"# Extraído automáticamente\n\n")
        for track in tracks:
            f.write(f"{track}\n")

    print(f"✓ Lista creada: {output_file} ({len(tracks)} canciones)")
    return output_file


def download_tracks(track_file):
    """Descarga los tracks usando el sistema mejorado"""
    print(f"\n{'='*60}")
    print(f"  Iniciando descarga con filtros de calidad")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(
            ["./download.sh", track_file],
            check=True
        )

        print(f"\n✓ Descarga completada exitosamente!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error en descarga: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python spotify_to_rekordbox.py <url_playlist_spotify>")
        print("\nEjemplo:")
        print("  python spotify_to_rekordbox.py https://open.spotify.com/playlist/3J1JiWN4zJcFPaCSWQSJMP")
        sys.exit(1)

    playlist_url = sys.argv[1]

    print(f"{'='*60}")
    print(f"  Spotify to Rekordbox - Pipeline Automático")
    print(f"{'='*60}\n")

    # Paso 1: Extraer tracks de Spotify
    tracks = get_spotify_tracks(playlist_url)

    if not tracks:
        print("❌ No se pudieron extraer tracks de Spotify")
        print("\nPosibles soluciones:")
        print("1. Verifica que la URL de la playlist sea correcta")
        print("2. Asegúrate de que la playlist sea pública o tengas acceso")
        print("3. Revisa tu autenticación con Spotify")
        sys.exit(1)

    print(f"\n✓ {len(tracks)} tracks extraídos de Spotify")

    # Paso 2: Crear archivo de lista
    track_file = create_download_list(tracks)

    # Paso 3: Confirmar con usuario
    print(f"\n{'='*60}")
    print(f"  Lista de canciones a descargar:")
    print(f"{'='*60}")
    for i, track in enumerate(tracks[:10], 1):
        print(f"  {i}. {track}")
    if len(tracks) > 10:
        print(f"  ... y {len(tracks) - 10} más")

    print(f"\n{'='*60}")
    print(f"  Filtros activos:")
    print(f"{'='*60}")
    print(f"  ✓ Omitir versiones UNRELEASED")
    print(f"  ✓ Omitir versiones LIVE")
    print(f"  ✓ Omitir tracks < 1:30 min")
    print(f"  ✓ Detección automática de KEY")
    print(f"  ✓ Metadatos ID3 completos")

    response = input(f"\n¿Continuar con la descarga? [Y/n]: ").lower()

    if response in ['', 'y', 'yes', 's', 'si']:
        # Paso 4: Descargar
        success = download_tracks(track_file)

        if success:
            print(f"\n{'='*60}")
            print(f"  ¡Pipeline completado exitosamente!")
            print(f"{'='*60}")
            print(f"\n📁 Canciones en: C:\\Users\\danie\\Music\\RekordboxDownloads\\")
            print(f"\n💡 Próximos pasos:")
            print(f"  1. Abre Rekordbox")
            print(f"  2. Archivo > Importar > Importar Carpeta")
            print(f"  3. Selecciona: C:\\Users\\danie\\Music\\RekordboxDownloads\\")
            print(f"  4. Analiza los tracks (BPM, beatgrid, KEY)")
        else:
            print(f"\n❌ Descarga cancelada o falló")
    else:
        print(f"\n❌ Descarga cancelada por el usuario")


if __name__ == "__main__":
    main()
