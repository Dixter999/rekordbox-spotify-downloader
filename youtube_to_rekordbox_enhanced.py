#!/usr/bin/env python3
"""
YouTube to Rekordbox MP3 Downloader - Enhanced Version
With quality filters, musical KEY detection and minimum duration
"""

import os
import sys
import subprocess
import re
import json
from pathlib import Path


class YouTubeToRekordbox:
    def __init__(self, output_dir="rekordbox_music", min_duration=90, main_folder=None, prefer_lyrics=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.failed_downloads = []
        self.skipped_songs = []
        self.min_duration = min_duration  # Minimum duration in seconds (1:30 = 90s)
        self.main_folder = main_folder  # Main folder for grouping (HOUSE, POP, etc)
        self.prefer_lyrics = prefer_lyrics  # Prefer lyrics videos over official videos

    def sanitize_filename(self, name):
        """Cleans filenames to avoid problematic characters"""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()

    def parse_song_line(self, line):
        """Parse a line from the file: 'Artista - Canción'"""
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
        """Checks if the song should be skipped due to quality filters"""
        title_lower = title.lower()

        # Low quality filters
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
                return True, f"contains '{keyword}'"

        return False, None

    def search_with_lyrics_priority(self, artist, song):
        """Search for lyrics video first, fallback to audio if not found or invalid.

        Lyrics videos typically have clean audio without sound effects from music videos
        (footsteps, ambient sounds, etc.), making them better for DJ use.

        Returns:
            tuple: (video_info dict, search_query used) or (None, None) if not found
        """
        if self.prefer_lyrics:
            # Priority 1: Try lyrics video
            lyrics_query = f"ytsearch1:{artist} {song} lyrics"
            video_info = self.get_video_info(lyrics_query)

            if video_info and self._is_relevant_result(video_info, artist, song):
                print(f"    🎤 Found lyrics version")
                return video_info, lyrics_query

            # Priority 2: Fallback to audio search
            print(f"    ℹ No lyrics version found, trying audio...")

        audio_query = f"ytsearch1:{artist} {song} audio"
        video_info = self.get_video_info(audio_query)

        return video_info, audio_query

    def _is_relevant_result(self, video_info, artist, song):
        """Check if the search result is relevant to the requested song.

        Validates that the found video title contains at least part of the
        artist name or song title to avoid completely unrelated results.
        """
        if not video_info:
            return False

        title_lower = video_info.get('title', '').lower()
        artist_lower = artist.lower()
        song_lower = song.lower()

        # Check if either artist or song appears in the title
        artist_words = artist_lower.split()
        song_words = song_lower.split()

        # At least one significant word from artist or song should be in the title
        artist_match = any(word in title_lower for word in artist_words if len(word) > 2)
        song_match = any(word in title_lower for word in song_words if len(word) > 2)

        return artist_match or song_match

    def get_video_info(self, search_query):
        """Gets video information before downloading"""
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
            print(f"    ⚠ Could not get video info: {str(e)}")

        return None

    def musical_to_camelot(self, key_str):
        """Converts musical notation (C# major) to Camelot (8B)"""
        # Mapeo de notas y escalas to Camelot
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
        """Detecta la KEY musical usando essentia y convierte to Camelot"""
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
                    # Convertir to Camelot
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
        # If main folder is defined, use that instead of artist folders
        if self.main_folder:
            artist_dir = self.output_dir / self.main_folder
        else:
            artist_clean = self.sanitize_filename(artist)
            artist_dir = self.output_dir / artist_clean

        # Crear directorio con manejo de errores para symlinks
        try:
            artist_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"    ⚠ Error creating folder, using alternative")
            if not self.main_folder:
                artist_clean = re.sub(r'[&]', 'and', artist_clean)
                artist_dir = self.output_dir / artist_clean
            artist_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n[{index}/{total}] Processing: {artist} - {song}")
        print(f"    Folder: {artist_dir}")

        # Step 1: Search with lyrics priority (if enabled)
        print(f"    🔍 Searching for video...")
        video_info, search_query = self.search_with_lyrics_priority(artist, song)

        if not video_info:
            print(f"    ✗ No se pudo encontrar el video")
            self.failed_downloads.append(f"{artist} - {song}")
            return False

        # Paso 2: Verificar filtros de calidad
        should_skip, reason = self.should_skip_song(video_info['title'])
        if should_skip:
            print(f"    ⊘ OMITIDO: {reason}")
            print(f"    Title: {video_info['title']}")
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
        print(f"    ✓ Title: {video_info['title']}")
        print(f"    ⏱ Duration: {duration // 60}:{duration % 60:02d}")
        print(f"    ⬇ Downloading...")

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

                    print(f"    🎵 Detecting musical KEY...")
                    key = self.detect_key(str(latest_file))

                    if key:
                        print(f"    🎹 KEY detected: {key}")
                        self.add_key_metadata(str(latest_file), key)
                    else:
                        print(f"    ℹ KEY not detected (requires essentia)")

                print(f"    ✓ Downloaded successfully")
                return True
            else:
                print(f"    ✗ Download error")
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
        """Processes the file with the song list"""
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
            print("No valid songs found in file")
            return

        print(f"═══════════════════════════════════════════════")
        print(f"  YouTube to Rekordbox MP3 Downloader Enhanced")
        print(f"═══════════════════════════════════════════════")
        print(f"Total songs: {len(songs)}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Min duration: {self.min_duration // 60}:{self.min_duration % 60:02d}")
        print(f"Prefer lyrics: {'Yes' if self.prefer_lyrics else 'No'}")
        print(f"Filters: UNRELEASED, Live, duration < {self.min_duration}s")
        print(f"═══════════════════════════════════════════════\n")

        for i, (artist, song) in enumerate(songs, 1):
            self.download_song(artist, song, i, len(songs))

        # Final summary
        print(f"\n{'═'*50}")
        print(f"  RESUMEN DE DESCARGAS")
        print(f"{'═'*50}")
        print(f"Total processed: {len(songs)}")
        print(f"✓ Successful: {len(songs) - len(self.failed_downloads) - len(self.skipped_songs)}")
        print(f"⊘ Skippeds: {len(self.skipped_songs)}")
        print(f"✗ Failed: {len(self.failed_downloads)}")

        if self.skipped_songs:
            print(f"\n⊘ Songs skipped (baja calidad):")
            for song in self.skipped_songs:
                print(f"   - {song}")

        if self.failed_downloads:
            print(f"\n✗ Canciones que fallaron:")
            for song in self.failed_downloads:
                print(f"   - {song}")

        print(f"\n📁 Canciones guardadas en: {self.output_dir.absolute()}")
        print(f"\n💡 Next step: Import the folder into Rekordbox")
        print(f"💡 Para KEY detection: pip install essentia mutagen")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='YouTube to Rekordbox MP3 Downloader - Enhanced Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_to_rekordbox_enhanced.py my_songs.txt
  python youtube_to_rekordbox_enhanced.py my_songs.txt --min-duration 120 --folder HOUSE
  python youtube_to_rekordbox_enhanced.py my_songs.txt --no-lyrics
        """
    )

    parser.add_argument('song_file', help='Text file with songs in format: Artist - Song')
    parser.add_argument('--min-duration', type=int, default=90,
                        help='Minimum song duration in seconds (default: 90)')
    parser.add_argument('--folder', dest='main_folder', default=None,
                        help='Main folder name for grouping downloads (e.g., HOUSE, POP)')
    parser.add_argument('--output', dest='output_dir', default='rekordbox_music',
                        help='Output directory (default: rekordbox_music)')

    # Lyrics preference group
    lyrics_group = parser.add_mutually_exclusive_group()
    lyrics_group.add_argument('--prefer-lyrics', dest='prefer_lyrics', action='store_true',
                              default=True, help='Prefer lyrics videos over official videos (default)')
    lyrics_group.add_argument('--no-lyrics', dest='prefer_lyrics', action='store_false',
                              help='Do not prefer lyrics videos, search for audio instead')

    # Backwards compatibility: support positional arguments
    parser.add_argument('legacy_duration', nargs='?', type=int, default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('legacy_folder', nargs='?', default=None,
                        help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Handle legacy positional arguments for backwards compatibility
    min_duration = args.legacy_duration if args.legacy_duration is not None else args.min_duration
    main_folder = args.legacy_folder if args.legacy_folder is not None else args.main_folder

    downloader = YouTubeToRekordbox(
        output_dir=args.output_dir,
        min_duration=min_duration,
        main_folder=main_folder,
        prefer_lyrics=args.prefer_lyrics
    )
    downloader.process_file(args.song_file)


if __name__ == "__main__":
    main()

