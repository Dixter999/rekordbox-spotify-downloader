#!/usr/bin/env python3
"""
YouTube to Rekordbox MP3 Downloader - Enhanced Version
Con filtros de calidad, detección de KEY musical y duración mínima
"""

import os
import sys
import subprocess
import re
import json
from pathlib import Path


class YouTubeToRekordbox:
    def __init__(self, output_dir="rekordbox_music", min_duration=90, main_folder=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.failed_downloads = []
        self.skipped_songs = []
        self.min_duration = min_duration  # Duración mínima en segundos (1:30 = 90s)
        self.main_folder = main_folder  # Carpeta principal para agrupar (HOUSE, POP, etc)

    def sanitize_filename(self, name):
        """Limpia nombres de archivo para evitar caracteres problemáticos"""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()

    def parse_song_line(self, line):
        """Parse una línea del archivo: 'Artista - Canción'"""
        line = line.strip()
        if not line or line.startswith('#'):
            return None, None

        if ' - ' in line:
            parts = line.split(' - ', 1)
            artist = parts[0].strip()
            song = parts[1].strip()
        else:
            artist = "Unknown"
            song = line

        return artist, song

    def should_skip_song(self, title):
        """Verifica si la canción debe ser omitida por filtros de calidad"""
        title_lower = title.lower()

        # Filtros de baja calidad
        skip_keywords = [
            'unreleased',
            'live',
            'live at',
            'live from',
            'live in',
            'concert',
            'tour',
            'remix live',
            'bootleg live'
        ]

        for keyword in skip_keywords:
            if keyword in title_lower:
                return True, f"contiene '{keyword}'"

        return False, None

    def get_video_info(self, search_query):
        """Obtiene información del video antes de descargar"""
        try:
            ytdlp_path = "venv/bin/yt-dlp" if os.path.exists("venv/bin/yt-dlp") else "yt-dlp"

            cmd = [
                ytdlp_path,
                "-j",  # JSON output
                "--no-playlist",
                search_query
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                info = json.loads(result.stdout)
                return {
                    'title': info.get('title', ''),
                    'duration': info.get('duration', 0),
                    'id': info.get('id', ''),
                    'uploader': info.get('uploader', '')
                }
        except Exception as e:
            print(f"    ⚠ No se pudo obtener info del video: {str(e)}")

        return None

    def musical_to_camelot(self, key_str):
        """Convierte notación musical (C# major) a Camelot (8B)"""
        # Mapeo de notas y escalas a Camelot
        camelot_map = {
            # Major keys (B suffix)
            'C major': '8B',
            'G major': '9B',
            'D major': '10B',
            'A major': '11B',
            'E major': '12B',
            'B major': '1B',
            'F# major': '2B',
            'Gb major': '2B',
            'Db major': '3B',
            'C# major': '3B',
            'Ab major': '4B',
            'Eb major': '5B',
            'Bb major': '6B',
            'F major': '7B',

            # Minor keys (A suffix)
            'A minor': '8A',
            'E minor': '9A',
            'B minor': '10A',
            'F# minor': '11A',
            'Gb minor': '11A',
            'C# minor': '12A',
            'Db minor': '12A',
            'Ab minor': '1A',
            'G# minor': '1A',
            'Eb minor': '2A',
            'D# minor': '2A',
            'Bb minor': '3A',
            'A# minor': '3A',
            'F minor': '4A',
            'C minor': '5A',
            'G minor': '6A',
            'D minor': '7A',
        }

        return camelot_map.get(key_str, key_str)

    def detect_key(self, audio_file):
        """Detecta la KEY musical usando essentia y convierte a Camelot"""
        try:
            # Intentar con essentia primero (más preciso para KEY)
            cmd = [
                "python3", "-c",
                f"""
import sys
try:
    import essentia.standard as es
    audio = es.MonoLoader(filename='{audio_file}')()
    key_extractor = es.KeyExtractor()
    key, scale, strength = key_extractor(audio)
    print(f"{{key}} {{scale}}")
except ImportError:
    print("ESSENTIA_NOT_INSTALLED")
except Exception as e:
    print(f"ERROR: {{e}}")
"""
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and "ESSENTIA_NOT_INSTALLED" not in result.stdout:
                key_info = result.stdout.strip()
                if key_info and "ERROR" not in key_info:
                    # Convertir a Camelot
                    camelot_key = self.musical_to_camelot(key_info)
                    return camelot_key

            # Fallback: usar librosa (menos preciso pero más común)
            print("    ℹ Essentia no disponible, intentando con análisis básico...")
            return None

        except Exception as e:
            print(f"    ⚠ Error detectando KEY: {str(e)}")
            return None

    def add_key_metadata(self, audio_file, key):
        """Agrega la KEY como metadata al archivo MP3"""
        try:
            # Usar eyeD3 o mutagen para agregar metadatos
            cmd = [
                "python3", "-c",
                f"""
import sys
try:
    from mutagen.id3 import ID3, TKEY
    audio = ID3('{audio_file}')
    audio.add(TKEY(encoding=3, text='{key}'))
    audio.save()
    print("OK")
except ImportError:
    print("MUTAGEN_NOT_INSTALLED")
except Exception as e:
    print(f"ERROR: {{e}}")
"""
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if "OK" in result.stdout:
                return True
            elif "MUTAGEN_NOT_INSTALLED" in result.stdout:
                print("    ℹ Mutagen no instalado, KEY no agregada a metadatos")
                print("    💡 Instala con: pip install mutagen")

            return False

        except Exception as e:
            print(f"    ⚠ Error agregando KEY a metadatos: {str(e)}")
            return False

    def download_song(self, artist, song, index, total):
        """Descarga una canción usando yt-dlp con filtros de calidad"""
        # Si hay una carpeta principal definida, usar esa en lugar de por artista
        if self.main_folder:
            artist_dir = self.output_dir / self.main_folder
        else:
            artist_clean = self.sanitize_filename(artist)
            artist_dir = self.output_dir / artist_clean

        # Crear directorio con manejo de errores para symlinks
        try:
            artist_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"    ⚠ Error creando carpeta, usando alternativa")
            if not self.main_folder:
                artist_clean = re.sub(r'[&]', 'and', artist_clean)
                artist_dir = self.output_dir / artist_clean
            artist_dir.mkdir(parents=True, exist_ok=True)

        search_query = f"ytsearch1:{artist} {song} audio"

        print(f"\n[{index}/{total}] Procesando: {artist} - {song}")
        print(f"    Carpeta: {artist_dir}")

        # Paso 1: Obtener información del video
        print(f"    🔍 Buscando video...")
        video_info = self.get_video_info(search_query)

        if not video_info:
            print(f"    ✗ No se pudo encontrar el video")
            self.failed_downloads.append(f"{artist} - {song}")
            return False

        # Paso 2: Verificar filtros de calidad
        should_skip, reason = self.should_skip_song(video_info['title'])
        if should_skip:
            print(f"    ⊘ OMITIDO: {reason}")
            print(f"    Título: {video_info['title']}")
            self.skipped_songs.append(f"{artist} - {song} ({reason})")
            return False

        # Paso 3: Verificar duración mínima
        duration = video_info.get('duration', 0)
        if duration > 0 and duration < self.min_duration:
            minutes = duration // 60
            seconds = duration % 60
            print(f"    ⊘ OMITIDO: duración muy corta ({minutes}:{seconds:02d})")
            self.skipped_songs.append(f"{artist} - {song} (duración: {minutes}:{seconds:02d})")
            return False

        # Paso 4: Descargar
        print(f"    ✓ Título: {video_info['title']}")
        print(f"    ⏱ Duración: {duration // 60}:{duration % 60:02d}")
        print(f"    ⬇ Descargando...")

        try:
            ytdlp_path = "venv/bin/yt-dlp" if os.path.exists("venv/bin/yt-dlp") else "yt-dlp"

            output_template = str(artist_dir / "%(title)s.%(ext)s")

            cmd = [
                ytdlp_path,
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "--embed-thumbnail",
                "--add-metadata",
                "--metadata-from-title", "%(artist)s - %(title)s",
                "--parse-metadata", f"title:{artist}",
                "-o", output_template,
                "--no-playlist",
                "--quiet",
                "--progress",
                search_query
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # Paso 5: Detectar KEY musical
                downloaded_files = list(artist_dir.glob("*.mp3"))
                if downloaded_files:
                    latest_file = max(downloaded_files, key=os.path.getctime)

                    print(f"    🎵 Detectando KEY musical...")
                    key = self.detect_key(str(latest_file))

                    if key:
                        print(f"    🎹 KEY detectada: {key}")
                        self.add_key_metadata(str(latest_file), key)
                    else:
                        print(f"    ℹ KEY no detectada (requiere essentia)")

                print(f"    ✓ Descargado exitosamente")
                return True
            else:
                print(f"    ✗ Error en descarga")
                if result.stderr:
                    print(f"    Error: {result.stderr[:200]}")
                self.failed_downloads.append(f"{artist} - {song}")
                return False

        except FileNotFoundError:
            print("\n¡ERROR! yt-dlp no está instalado.")
            print("Instálalo con: pip install yt-dlp")
            sys.exit(1)
        except Exception as e:
            print(f"    ✗ Error: {str(e)}")
            self.failed_downloads.append(f"{artist} - {song}")
            return False

    def process_file(self, input_file):
        """Procesa el archivo con la lista de canciones"""
        if not Path(input_file).exists():
            print(f"Error: El archivo '{input_file}' no existe")
            return

        songs = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                artist, song = self.parse_song_line(line)
                if artist and song:
                    songs.append((artist, song))

        if not songs:
            print("No se encontraron canciones válidas en el archivo")
            return

        print(f"═══════════════════════════════════════════════")
        print(f"  YouTube to Rekordbox MP3 Downloader Enhanced")
        print(f"═══════════════════════════════════════════════")
        print(f"Total de canciones: {len(songs)}")
        print(f"Directorio de salida: {self.output_dir.absolute()}")
        print(f"Duración mínima: {self.min_duration // 60}:{self.min_duration % 60:02d}")
        print(f"Filtros: UNRELEASED, Live, duración < 1:30")
        print(f"═══════════════════════════════════════════════\n")

        for i, (artist, song) in enumerate(songs, 1):
            self.download_song(artist, song, i, len(songs))

        # Resumen final
        print(f"\n{'═'*50}")
        print(f"  RESUMEN DE DESCARGAS")
        print(f"{'═'*50}")
        print(f"Total procesadas: {len(songs)}")
        print(f"✓ Exitosas: {len(songs) - len(self.failed_downloads) - len(self.skipped_songs)}")
        print(f"⊘ Omitidas: {len(self.skipped_songs)}")
        print(f"✗ Fallidas: {len(self.failed_downloads)}")

        if self.skipped_songs:
            print(f"\n⊘ Canciones omitidas (baja calidad):")
            for song in self.skipped_songs:
                print(f"   - {song}")

        if self.failed_downloads:
            print(f"\n✗ Canciones que fallaron:")
            for song in self.failed_downloads:
                print(f"   - {song}")

        print(f"\n📁 Canciones guardadas en: {self.output_dir.absolute()}")
        print(f"\n💡 Próximo paso: Importa la carpeta en Rekordbox")
        print(f"💡 Para KEY detection: pip install essentia mutagen")


def main():
    if len(sys.argv) < 2:
        print("Uso: python youtube_to_rekordbox_enhanced.py <archivo_canciones.txt> [duracion_minima] [carpeta_principal]")
        print("\nEjemplo:")
        print("  python youtube_to_rekordbox_enhanced.py mis_canciones.txt")
        print("  python youtube_to_rekordbox_enhanced.py mis_canciones.txt 120 HOUSE")
        sys.exit(1)

    input_file = sys.argv[1]
    min_duration = int(sys.argv[2]) if len(sys.argv) > 2 else 90  # Default 1:30
    main_folder = sys.argv[3] if len(sys.argv) > 3 else None  # Carpeta principal opcional
    output_dir = "rekordbox_music"

    downloader = YouTubeToRekordbox(output_dir, min_duration, main_folder)
    downloader.process_file(input_file)


if __name__ == "__main__":
    main()
