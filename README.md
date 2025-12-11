# Rekordbox Spotify Downloader 🎵🎧

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**The ultimate solution for DJs to download and organize music from YouTube with Spotify playlist integration, optimized for Pioneer Rekordbox.**

Transform your Spotify playlists into a fully organized DJ library with automatic KEY detection (Camelot notation), BPM analysis, and quality filtering - perfect for harmonic mixing!

---

## 💡 Why This Project Exists

As a DJ, I faced a critical limitation: **Rekordbox doesn't allow editing tracks from Spotify streaming**. You can't analyze cue points, loops, or hot cues on Spotify tracks - you need local files.

The problem? Manually downloading hundreds of songs from Spotify playlists was tedious and time-consuming.

**The Solution:** I discovered two amazing open-source projects:
- **[spotify-backup](https://github.com/caseychu/spotify-backup)** by [@caseychu](https://github.com/caseychu) - Extract Spotify playlists to JSON
- **[ytm-dlapi](https://github.com/Thanatoslayer6/ytm-dlapi)** - YouTube Music download concept

I combined and enhanced these tools with:
- ✨ **Automatic KEY detection** using Essentia (Camelot notation for harmonic mixing)
- 🥁 **BPM analysis** for perfect beatmatching
- 🎯 **Quality filtering** (removes LIVE versions, UNRELEASED tracks, short clips)
- 📚 **Smart organization** (by genre, artist, or custom folders)
- 🔄 **Batch processing** for hundreds of songs at once

Now you can build a complete Rekordbox library from your Spotify playlists with full editing capabilities!

---

## ✨ Features

### 🎹 **Advanced Music Analysis**
- **Automatic KEY Detection** in Camelot notation (1A-12A, 1B-12B) using Essentia
- **BPM Detection** for perfect beatmatching
- **ID3 Metadata Tagging** compatible with Rekordbox
- **Lyrics Video Priority** - Downloads lyrics videos for cleaner audio (no video SFX)
- **Audio Quality Filtering** (removes UNRELEASED, LIVE versions)
- **Duration Filtering** (configurable minimum length, default 1:30)

### 📚 **Smart Organization**
- **Folder-based Organization** (HOUSE, POP, Artist folders, etc.)
- **Batch Processing** of entire Spotify playlists
- **Automatic MP3 Conversion** from YouTube audio
- **CSV to TXT Converter** for Exportify playlists
- **Windows/WSL Integration** for seamless cross-platform usage

### 🎼 **Spotify Integration**
- **[Exportify](https://exportify.net/) Support** - Export playlists to CSV, convert to song list
- **Extract Playlists** directly from your Spotify library
- **Filter by Genre** (HOUSE, POP, or custom categories)
- **OAuth Authentication** for secure access (optional)
- **Backup Your Music Library** to JSON format

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **FFmpeg** (for audio conversion)
- **WSL** (if using Windows)
- **Spotify Account** (for playlist extraction)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Dixter999/rekordbox-spotify-downloader.git
cd rekordbox-spotify-downloader
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install system dependencies:**
```bash
# Ubuntu/Debian/WSL
sudo apt update
sudo apt install ffmpeg build-essential libeigen3-dev libfftw3-dev \
    libavcodec-dev libavformat-dev libavutil-dev libswresample-dev \
    libsamplerate0-dev libtag1-dev libyaml-dev python3-dev

# macOS
brew install ffmpeg eigen fftw libsamplerate libyaml
```

---

## 📖 Usage

> **⚠️ Important Note About Repositories:**
>
> This project uses **TWO separate repositories**:
> 1. **This repo** (rekordbox-spotify-downloader) - Main tool for downloading and KEY detection
> 2. **[spotify-backup](https://github.com/caseychu/spotify-backup)** - Third-party tool for extracting Spotify playlists (only needed if you use Option 2)
>
> **If you don't use Spotify playlists**, you only need this repo (Option 1)!

---

### Option 1: Download from a Simple Song List (No Spotify Needed)

**1. Create a text file with song names:**

`songs.txt`:
```
Martin Garrix - Animals
Lost Frequencies - Are You With Me
Avicii - Levels
David Guetta, Bebe Rexha - I'm Good (Blue)
```

**2. Download with KEY and BPM detection:**
```bash
source venv/bin/activate
python3 youtube_to_rekordbox_enhanced.py songs.txt
```

**3. Organize by folder (optional):**
```bash
# Download into HOUSE folder
python3 youtube_to_rekordbox_enhanced.py house_songs.txt --folder HOUSE

# Download into POP folder with custom min duration
python3 youtube_to_rekordbox_enhanced.py pop_songs.txt --min-duration 120 --folder POP

# Disable lyrics video preference (search for "audio" instead)
python3 youtube_to_rekordbox_enhanced.py songs.txt --no-lyrics
```

---

### Option 2: Export from Spotify with Exportify (Recommended)

The easiest way to get your Spotify playlists!

**1. Go to [Exportify](https://exportify.net/):**
- Log in with your Spotify account
- Click "Export" on any playlist to download a CSV file

**2. Convert CSV to song list:**
```bash
python3 convert_csv_to_txt.py my_playlist.csv
# Creates: my_playlist.txt
```

**3. Download the songs:**
```bash
python3 youtube_to_rekordbox_enhanced.py my_playlist.txt --folder HOUSE
```

**That's it!** No OAuth setup, no API keys - just export and download.

---

### Option 3: Extract from Your Spotify Playlists (Advanced)

For more control, you can use the spotify-backup tool:

**1. Get your Spotify data:**

First, clone the spotify-backup tool (only needs to be done once):
```bash
git clone https://github.com/caseychu/spotify-backup.git
```

Then authenticate with your Spotify account:
```bash
cd spotify-backup
python3 spotify-backup.py youremail@example.com
cd ..
```

This will:
- Open your browser for Spotify OAuth login
- Download all your playlists to a JSON file: `youremail@example_2025_11_13.json`

**2. Extract specific playlists:**

```bash
python3 extract_spotify_playlists.py spotify-backup/youremail@example_2025_11_13.json
```

The script will ask which playlists you want to extract. It creates text files like:
- `spotify_HOUSE.txt`
- `spotify_POP.txt`
- etc.

**3. Download the songs:**
```bash
# Download HOUSE playlist
python3 youtube_to_rekordbox_enhanced.py spotify_HOUSE.txt 90 HOUSE

# Download POP playlist
python3 youtube_to_rekordbox_enhanced.py spotify_POP.txt 90 POP
```

---

### Simple 3-Step Workflow Summary

```bash
# Step 1: Get your Spotify playlists (one-time setup)
git clone https://github.com/caseychu/spotify-backup.git
cd spotify-backup && python3 spotify-backup.py youremail@example.com && cd ..

# Step 2: Extract the playlists you want
python3 extract_spotify_playlists.py spotify-backup/youremail@example_2025_11_13.json

# Step 3: Download with KEY/BPM detection
python3 youtube_to_rekordbox_enhanced.py spotify_HOUSE.txt 90 HOUSE
```

Done! Your music is now in `rekordbox_music/HOUSE/` with KEY (Camelot) and BPM tags.

### 3. Update Metadata for Existing Files

**Update KEY and BPM for all folders:**
```bash
./update_all_metadata.sh
```

**Update specific folder:**
```bash
python update_metadata.py /path/to/your/music/folder
```

---

## 📁 Project Structure

```
rekordbox-spotify-downloader/
├── youtube_to_rekordbox_enhanced.py    # Main download script with filters
├── convert_csv_to_txt.py               # Convert Exportify CSV to song list
├── update_metadata.py                   # Update KEY/BPM for existing files
├── update_all_metadata.sh              # Batch metadata updater
├── extract_spotify_playlists.py        # Extract playlists from JSON
├── spotify-backup/                     # Spotify OAuth integration (optional)
│   └── spotify-backup.py               # Backup Spotify library
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── LICENSE                             # MIT License
└── examples/                           # Example song lists
    ├── example_house.txt
    ├── example_pop.txt
    └── martin_garrix_set.txt
```

---

## 🎛️ Configuration

### Quality Filters

The downloader automatically filters out:
- **UNRELEASED** tracks
- **LIVE** versions (concert recordings)
- Songs **shorter than 90 seconds** (configurable)

Edit `youtube_to_rekordbox_enhanced.py` to customize:
```python
skip_keywords = [
    'unreleased',
    'live',
    'live at',
    'concert',
    'tour'
]
```

### Output Directory

Default: `rekordbox_music/`

To use a Windows path with WSL:
```bash
ln -s /mnt/c/Users/YOUR_USERNAME/Music/RekordboxDownloads rekordbox_music
```

---

## 🎹 Camelot Key Notation

The system uses **Camelot Wheel notation** for harmonic mixing:

| Musical Key | Camelot | Musical Key | Camelot |
|-------------|---------|-------------|---------|
| C major     | 8B      | A minor     | 8A      |
| G major     | 9B      | E minor     | 9A      |
| D major     | 10B     | B minor     | 10A     |
| A major     | 11B     | F# minor    | 11A     |
| E major     | 12B     | C# minor    | 12A     |
| B major     | 1B      | G# minor    | 1A      |
| F# major    | 2B      | D# minor    | 2A      |
| Db major    | 3B      | Bb minor    | 3A      |
| Ab major    | 4B      | F minor     | 4A      |
| Eb major    | 5B      | C minor     | 5A      |
| Bb major    | 6B      | G minor     | 6A      |
| F major     | 7B      | D minor     | 7A      |

**Harmonic Mixing Rules:**
- Mix tracks with the **same number** (e.g., 8A → 8B)
- Mix tracks **±1** on the wheel (e.g., 8A → 9A or 7A)

---

## 🔗 Tools & Dependencies

This project integrates several powerful tools:

### Core Tools
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube downloader (replaces youtube-dl)
- **[Essentia](https://essentia.upf.edu/)** - Music information retrieval for KEY and BPM detection
- **[Mutagen](https://mutagen.readthedocs.io/)** - Python library for audio metadata
- **[FFmpeg](https://ffmpeg.org/)** - Audio/video processing

### Spotify Integration
- **[spotify-backup](https://github.com/caseychu/spotify-backup)** - Backup Spotify playlists to JSON
- **[Spotify Web API](https://developer.spotify.com/documentation/web-api/)** - Access Spotify data

---

## 📊 Example Output

```
═══════════════════════════════════════════════
  YouTube to Rekordbox MP3 Downloader Enhanced
═══════════════════════════════════════════════

[1/267] Processing: Martin Garrix - Animals
    Folder: rekordbox_music/HOUSE
    🔍 Searching video...
    ✓ Title: Martin Garrix - Animals (Official Video)
    ⏱ Duration: 5:20
    ⬇ Downloading...
    🎵 Detecting musical KEY...
    🎹 KEY detected: 4A
    💾 BPM detected: 128
    ✓ Downloaded successfully
```

---

## 🛠️ Troubleshooting

### Issue: "Essentia not available"
**Solution:**
```bash
pip install essentia-tensorflow
```

### Issue: "FFmpeg not found"
**Solution:**
```bash
# Ubuntu/WSL
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Issue: "Permission denied" on Windows paths
**Solution:** Use WSL and symlink:
```bash
ln -s /mnt/c/Users/YOUR_USERNAME/Music rekordbox_music
```

### Issue: Downloads are in WEBM format
**Solution:** Ensure FFmpeg is installed and in PATH

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
git clone https://github.com/Dixter999/rekordbox-spotify-downloader.git
cd rekordbox-spotify-downloader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Areas for Contribution
- [ ] Add support for other music platforms (SoundCloud, Beatport)
- [ ] GUI interface
- [ ] Docker container
- [ ] Advanced playlist management
- [ ] Duplicate detection
- [ ] Waveform generation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is for **personal use only**. Please respect copyright laws and only download music you have the rights to access. Consider supporting artists by:

- Purchasing music on [Beatport](https://www.beatport.com/)
- Subscribing to [Spotify](https://www.spotify.com/)
- Buying tracks on [Bandcamp](https://bandcamp.com/)
- Supporting artists on [SoundCloud](https://soundcloud.com/)

**YouTube Terms of Service:** Review [YouTube's Terms of Service](https://www.youtube.com/t/terms) before using this tool.

---

## 🎯 Use Cases

### For DJs
- **Build your Rekordbox library** from Spotify playlists
- **Harmonic mixing** with automatic Camelot key detection
- **Organize by genre** (HOUSE, Techno, Pop, etc.)
- **Filter low-quality** live recordings and unreleased tracks

### For Music Producers
- **Sample collection** organized by key and BPM
- **Reference tracks** for your productions
- **Analyze song structure** with precise BPM data

### For Music Enthusiasts
- **Offline music library** from your Spotify favorites
- **High-quality MP3s** with proper metadata
- **Organized collection** by artist or genre

---

## 🙏 Acknowledgments

This project stands on the shoulders of amazing open-source work:

### Core Inspiration
- **[spotify-backup](https://github.com/caseychu/spotify-backup)** by [@caseychu](https://github.com/caseychu) - The foundation for Spotify playlist extraction
- **[ytm-dlapi](https://github.com/Thanatoslayer6/ytm-dlapi)** by [@Thanatoslayer6](https://github.com/Thanatoslayer6) - Initial concept for YouTube Music downloads

### Essential Tools
- **[yt-dlp team](https://github.com/yt-dlp/yt-dlp)** - Powerful YouTube downloader that makes this possible
- **[Music Technology Group (MTG)](https://www.upf.edu/web/mtg)** - Creators of Essentia for music analysis
- **[Mutagen contributors](https://mutagen.readthedocs.io/)** - Python audio metadata library
- **[FFmpeg team](https://ffmpeg.org/)** - Universal audio/video processing

### Special Thanks
- **Pioneer DJ** for creating Rekordbox, the best DJ software for professional mixing
- **The DJ community** for inspiring this project and providing feedback

---

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Dixter999/rekordbox-spotify-downloader/issues) page
2. Open a new issue with:
   - Your OS and Python version
   - Error message/log
   - Steps to reproduce

---

## 🌟 Star History

If this project helped you, please ⭐ star it on GitHub!

---

**Made with ❤️ for the DJ community**
