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

## 🚀 Quick Start (5 Minutes Setup)

### Step 1: Install the Tool

```bash
# Clone the repository
git clone https://github.com/Dixter999/rekordbox-spotify-downloader.git
cd rekordbox-spotify-downloader

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian/WSL)
sudo apt update && sudo apt install -y ffmpeg
```

<details>
<summary>📦 macOS Installation</summary>

```bash
brew install ffmpeg python3
```
</details>

<details>
<summary>📦 Full dependencies for KEY detection (optional)</summary>

```bash
# Ubuntu/Debian/WSL - for Essentia KEY detection
sudo apt install build-essential libeigen3-dev libfftw3-dev \
    libavcodec-dev libavformat-dev libavutil-dev libswresample-dev \
    libsamplerate0-dev libtag1-dev libyaml-dev python3-dev
```
</details>

---

### Step 2: Set Up the YouTube PO Token Provider (Required)

Since 2025, YouTube requires a **PO Token (Proof of Origin)** for downloads. Without it, every request hangs and times out (`No se pudo obtener info del video` / "could not get video info"). `yt-dlp` obtains this token from the [bgutil-ytdlp-pot-provider](https://github.com/Brainicism/bgutil-ytdlp-pot-provider) plugin (installed via `requirements.txt`), which needs a small companion Node.js server.

```bash
# Requires Node.js 20+ (check with: node --version)
git clone https://github.com/Brainicism/bgutil-ytdlp-pot-provider ~/bgutil-ytdlp-pot-provider
cd ~/bgutil-ytdlp-pot-provider/server
npm install
npx tsc        # builds build/generate_once.js  (there is no "npm run build")
cd -
```

`yt-dlp` automatically detects the script at `~/bgutil-ytdlp-pot-provider/server/build/generate_once.js` — no extra flags needed. Verify it works:

```bash
node ~/bgutil-ytdlp-pot-provider/server/build/generate_once.js --version   # prints the version
```

> **Note:** A harmless `WARNING: No supported JavaScript runtime could be found` may still appear during downloads. The bgutil `script-node` provider supplies the token regardless, so downloads succeed.

---

## 📖 How to Download Music (Step-by-Step)

### 🎯 Option 1: From Spotify Playlist (Recommended)

This is the easiest method - export your Spotify playlist and download all songs!

---

#### **Step 1: Export Your Spotify Playlist**

1. Open **[Exportify.net](https://exportify.net/)** in your browser
2. Click **"Get Started"** and log in with your Spotify account
3. Find your playlist and click the green **"Export"** button
4. A CSV file will download (e.g., `My_Playlist.csv`)

```
📁 Downloads/
   └── My_Playlist.csv   ← Downloaded from Exportify
```

---

#### **Step 2: Convert CSV to Song List**

Move the CSV file to your project folder and convert it:

```bash
# Activate the virtual environment
source venv/bin/activate

# Convert the CSV to a text file
python3 convert_csv_to_txt.py My_Playlist.csv
```

**Output:**
```
✓ Converted 85 songs from My_Playlist.csv
✓ Created: My_Playlist.txt
```

The text file looks like this:
```
# Converted from My_Playlist.csv
# Total songs: 85

Martin Garrix - Animals
Lost Frequencies - Are You With Me
Avicii - Levels
David Guetta - Titanium
...
```

---

#### **Step 3: Download All Songs**

Now download all songs to a folder (e.g., `HOUSE`):

```bash
python3 youtube_to_rekordbox_enhanced.py My_Playlist.txt --output rekordbox_music/HOUSE --prefer-lyrics
```

**Example Output:**
```
═══════════════════════════════════════════════
  YouTube to Rekordbox MP3 Downloader Enhanced
═══════════════════════════════════════════════
Total songs: 85
Output directory: /home/user/rekordbox_music/HOUSE
Duration filter: 1:30 - 10:00
Prefer lyrics: Yes
═══════════════════════════════════════════════

[1/85] Processing: Martin Garrix - Animals
    Folder: rekordbox_music/HOUSE
    🔍 Searching for video...
    🎤 Found lyrics version
    ✓ Title: Martin Garrix - Animals (Lyrics)
    ⏱ Duration: 5:04
    ⬇ Downloading...
    🎵 Detecting musical KEY...
    🎹 KEY detected: 4A
    ✓ Downloaded successfully

[2/85] Processing: Lost Frequencies - Are You With Me
    Folder: rekordbox_music/HOUSE
    🔍 Searching for video...
    🎤 Found lyrics version
    ✓ Title: Lost Frequencies - Are You With Me (Lyrics)
    ⏱ Duration: 2:22
    ⬇ Downloading...
    🎵 Detecting musical KEY...
    🎹 KEY detected: 4B
    ✓ Downloaded successfully

[3/85] Processing: Avicii - Levels
    ⏭ SKIPPED: Already exists as 'Levels (Lyrics).mp3'

...

══════════════════════════════════════════════════
  DOWNLOAD SUMMARY
══════════════════════════════════════════════════
Total processed: 85
✓ Downloaded: 72
⏭ Already existed: 10
⊘ Skipped (quality): 2
✗ Failed: 1

⊘ Songs skipped (low quality):
   - DJ Snake - Turn Down for What (too long: 12:34)
   - Random Artist - Live at Festival (contains: live)

📁 Songs saved to: /home/user/rekordbox_music/HOUSE

💡 Next step: Import the folder into Rekordbox
```

---

#### **Step 4: Import into Rekordbox**

1. Open **Rekordbox**
2. Go to **File → Import → Import Folder**
3. Select `rekordbox_music/HOUSE`
4. Your songs are now ready with **KEY** (Camelot notation) already tagged! 🎹

---

### 📝 Complete Example Workflow

```bash
# 1. Setup (only once)
git clone https://github.com/Dixter999/rekordbox-spotify-downloader.git
cd rekordbox-spotify-downloader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Download your playlist from Exportify.net and move it here
mv ~/Downloads/Summer_Hits_2025.csv .

# 3. Convert to song list
python3 convert_csv_to_txt.py Summer_Hits_2025.csv

# 4. Download all songs
python3 youtube_to_rekordbox_enhanced.py Summer_Hits_2025.txt --output rekordbox_music/SUMMER --prefer-lyrics

# 5. Done! Your music is in rekordbox_music/SUMMER/
ls rekordbox_music/SUMMER/
```

---

### 🎵 Option 2: From a Simple Text File

Don't have Spotify? Just create a text file manually:

**1. Create `my_songs.txt`:**
```
Martin Garrix - Animals
Avicii - Levels
Calvin Harris - Summer
David Guetta - Titanium
```

**2. Download:**
```bash
source venv/bin/activate
python3 youtube_to_rekordbox_enhanced.py my_songs.txt --output rekordbox_music/EDM --prefer-lyrics
```

---

### ⚙️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--output` | Output folder | `--output rekordbox_music/HOUSE` |
| `--prefer-lyrics` | Search for lyrics videos (cleaner audio) | `--prefer-lyrics` |
| `--no-lyrics` | Search for official/audio videos | `--no-lyrics` |
| `--min-duration` | Minimum song length in seconds | `--min-duration 120` |
| `--max-duration` | Maximum song length in seconds | `--max-duration 480` |

**Examples:**
```bash
# Download to HOUSE folder with lyrics preference
python3 youtube_to_rekordbox_enhanced.py playlist.txt --output rekordbox_music/HOUSE --prefer-lyrics

# Download with custom duration limits (2-8 minutes)
python3 youtube_to_rekordbox_enhanced.py playlist.txt --output rekordbox_music/POP --min-duration 120 --max-duration 480

# Download without lyrics preference
python3 youtube_to_rekordbox_enhanced.py playlist.txt --output rekordbox_music/EDM --no-lyrics
```

---

### 🔄 Update KEY/BPM for Existing Files

Already have MP3 files? Add KEY detection to them:

```bash
# Update all folders
./update_all_metadata.sh

# Update specific folder
python3 update_metadata.py rekordbox_music/HOUSE
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
- **[bgutil-ytdlp-pot-provider](https://github.com/Brainicism/bgutil-ytdlp-pot-provider)** - Generates YouTube PO Tokens so yt-dlp can fetch videos
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

### Issue: Downloads hang or time out ("could not get video info")
**Cause:** YouTube's PO Token requirement is not satisfied — the bgutil provider server isn't set up.
**Solution:** Complete [Step 2: Set Up the YouTube PO Token Provider](#step-2-set-up-the-youtube-po-token-provider-required). Ensure Node.js 20+ is installed and that this prints a version:
```bash
node ~/bgutil-ytdlp-pot-provider/server/build/generate_once.js --version
```

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
- [x] ~~Duplicate detection~~ ✅ Implemented!
- [ ] Waveform generation
- [ ] BPM detection integration

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
