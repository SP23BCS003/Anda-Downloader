# Video Downloader

A web-based video downloader supporting YouTube, Vimeo, Dailymotion, Twitter/X, and more.

## Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **FFmpeg** - Will be installed automatically by the backend script

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install FFmpeg (run once)
python check_and_install_ffmpeg.py

# Start the backend server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 3. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

## Supported Platforms

| Platform | Status |
|----------|--------|
| YouTube | ✅ Works |
| Vimeo | ✅ Works |
| Dailymotion | ✅ Works |
| Twitter/X | ✅ Works |
| SoundCloud | ✅ Works (Audio) |
| TikTok | ⚠️ Requires cookies |
| Instagram | ⚠️ Requires cookies |
| Facebook | ⚠️ Requires cookies |

## Troubleshooting

### FFmpeg not found
Run `python check_and_install_ffmpeg.py` in the backend folder.

### yt-dlp errors
Update yt-dlp: `pip install --upgrade yt-dlp`

### TikTok/Instagram/Facebook errors
These platforms require authentication. You need to export cookies from your browser.

## Project Structure

```
Downloader/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── check_and_install_ffmpeg.py
│   └── ffmpeg/              # FFmpeg binaries (after install)
└── frontend/
    ├── src/                 # React/Vue source code
    ├── package.json         # Node dependencies
    └── ...
```
