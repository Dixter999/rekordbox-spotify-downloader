#!/usr/bin/env python3
"""
Update BPM and KEY metadata for existing MP3 files
"""

import sys
import os
from pathlib import Path
import subprocess


class MetadataUpdater:
    def __init__(self):
        # Use venv python if available
        venv_python = Path("venv/bin/python3")
        self.python_path = str(venv_python) if venv_python.exists() else "python3"

        self.camelot_map = {
            # Major keys (B suffix)
            'C major': '8B', 'G major': '9B', 'D major': '10B', 'A major': '11B',
            'E major': '12B', 'B major': '1B', 'F# major': '2B', 'Gb major': '2B',
            'Db major': '3B', 'C# major': '3B', 'Ab major': '4B', 'Eb major': '5B',
            'Bb major': '6B', 'F major': '7B',
            # Minor keys (A suffix)
            'A minor': '8A', 'E minor': '9A', 'B minor': '10A', 'F# minor': '11A',
            'Gb minor': '11A', 'C# minor': '12A', 'Db minor': '12A', 'Ab minor': '1A',
            'G# minor': '1A', 'Eb minor': '2A', 'D# minor': '2A', 'Bb minor': '3A',
            'A# minor': '3A', 'F minor': '4A', 'C minor': '5A', 'G minor': '6A',
            'D minor': '7A',
        }

    def detect_key(self, audio_file):
        """Detect KEY using essentia"""
        try:
            cmd = [
                self.python_path, "-c",
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
                    return self.camelot_map.get(key_info, key_info)

            return None

        except Exception as e:
            print(f"    ⚠ Error detecting KEY: {str(e)}")
            return None

    def detect_bpm(self, audio_file):
        """Detect BPM using essentia"""
        try:
            cmd = [
                self.python_path, "-c",
                f"""
import sys
try:
    import essentia.standard as es
    audio = es.MonoLoader(filename='{audio_file}')()
    rhythm_extractor = es.RhythmExtractor2013()
    bpm, _, _, _, _ = rhythm_extractor(audio)
    print(f"{{int(bpm)}}")
except ImportError:
    print("ESSENTIA_NOT_INSTALLED")
except Exception as e:
    print(f"ERROR: {{e}}")
"""
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and "ESSENTIA_NOT_INSTALLED" not in result.stdout:
                bpm_info = result.stdout.strip()
                if bpm_info and "ERROR" not in bpm_info and bpm_info.isdigit():
                    return int(bpm_info)

            return None

        except Exception as e:
            print(f"    ⚠ Error detecting BPM: {str(e)}")
            return None

    def update_metadata(self, audio_file, key=None, bpm=None):
        """Update KEY and BPM metadata"""
        try:
            cmd = [
                self.python_path, "-c",
                f"""
import sys
try:
    from mutagen.id3 import ID3, TKEY, TBPM
    audio = ID3('{audio_file}')

    if '{key}' != 'None':
        audio.add(TKEY(encoding=3, text='{key}'))

    if '{bpm}' != 'None':
        audio.add(TBPM(encoding=3, text='{bpm}'))

    audio.save()
    print("OK")
except Exception as e:
    print(f"ERROR: {{e}}")
"""
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return "OK" in result.stdout

        except Exception as e:
            print(f"    ⚠ Error updating metadata: {str(e)}")
            return False

    def process_file(self, file_path, index, total):
        """Process a single file"""
        print(f"\n[{index}/{total}] {file_path.name}")

        # Detect KEY
        print("    🎹 Detecting KEY...", end=" ", flush=True)
        key = self.detect_key(str(file_path))
        if key:
            print(f"✓ {key}")
        else:
            print("✗ Not detected")

        # Detect BPM
        print("    🥁 Detecting BPM...", end=" ", flush=True)
        bpm = self.detect_bpm(str(file_path))
        if bpm:
            print(f"✓ {bpm}")
        else:
            print("✗ Not detected")

        # Update metadata
        if key or bpm:
            print("    💾 Updating metadata...", end=" ", flush=True)
            if self.update_metadata(str(file_path), key, bpm):
                print("✓")
                return True, key, bpm
            else:
                print("✗")
                return False, None, None

        return False, None, None

    def process_directory(self, directory):
        """Process all MP3 files in directory"""
        dir_path = Path(directory)
        mp3_files = list(dir_path.glob("*.mp3"))

        if not mp3_files:
            print(f"No se encontraron archivos MP3 en {directory}")
            return

        print(f"\n{'='*60}")
        print(f"  Processing: {directory}")
        print(f"  Total de archivos: {len(mp3_files)}")
        print(f"{'='*60}")

        updated = 0
        failed = 0

        for i, file_path in enumerate(mp3_files, 1):
            success, key, bpm = self.process_file(file_path, i, len(mp3_files))
            if success:
                updated += 1
            elif key is None and bpm is None:
                failed += 1

        print(f"\n{'='*60}")
        print(f"  Resumen: {directory}")
        print(f"  Actualizados: {updated}/{len(mp3_files)}")
        print(f"  Fallidos: {failed}/{len(mp3_files)}")
        print(f"{'='*60}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python update_metadata.py <directorio>")
        print("Ejemplo: python update_metadata.py rekordbox_music/HOUSE")
        sys.exit(1)

    directory = sys.argv[1]
    updater = MetadataUpdater()
    updater.process_directory(directory)


if __name__ == "__main__":
    main()
