from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, Response

from fastapi.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
import yt_dlp
import os
import uuid
import glob
import asyncio
import re
from pydantic import BaseModel
from typing import Dict, Any

# Import admin routes
from admin_routes import router as admin_router
from database import init_db, get_db
from init_db import create_default_data
from models import Settings
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    # Initialize database
    init_db()
    # Create default admin user and settings
    create_default_data()
    print("✓ Database initialized")
    
    # Cleanup old files
    files = glob.glob("downloads/*")
    for f in files:
        if os.path.isfile(f):
            os.remove(f)
            
    # Add local ffmpeg to PATH
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    if os.path.exists(ffmpeg_dir):
        print(f"Adding {ffmpeg_dir} to PATH")
        os.environ["PATH"] += os.pathsep + ffmpeg_dir

# Mount admin routes
app.include_router(admin_router)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=None, status_code=204)

# In-memory job store (for simplicity)
# Structure: job_id -> { status: 'pending'|'downloading'|'completed'|'error', progress: int, filename: str, error: str }
download_jobs: Dict[str, Any] = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    format_id: str
    start_time: str = None
    end_time: str = None

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {e}")

def my_hook(d):
    job_id = d.get('info_dict', {}).get('_job_id')
    if not job_id: return
    
    if d['status'] == 'downloading':
        # Calculate progress
        try:
            p = d.get('_percent_str', '0%').replace('%','')
            download_jobs[job_id]['progress'] = float(p)
            download_jobs[job_id]['status'] = 'downloading'
        except:
            pass
    elif d['status'] == 'finished':
        download_jobs[job_id]['progress'] = 100
        download_jobs[job_id]['status'] = 'processing' # Processing/Converting

def parse_time(t_str):
    """Converts HH:MM:SS to seconds"""
    if not t_str: return 0
    parts = list(map(int, t_str.split(':')))
    if len(parts) == 3:
        return parts[0]*3600 + parts[1]*60 + parts[2]
    elif len(parts) == 2:
        return parts[0]*60 + parts[1]
    return parts[0]

def process_download(job_id: str, url: str, format_id: str, start_time: str = None, end_time: str = None):
    try:
        download_jobs[job_id]['status'] = 'downloading'
        filename_base = f"temp_{job_id}"
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': f"{filename_base}.%(ext)s",
            'quiet': True,
            'nocheckcertificate': True,
        }

        ffmpeg_local = os.path.join(os.getcwd(), "ffmpeg")
        if os.path.exists(ffmpeg_local):
            ydl_opts['ffmpeg_location'] = ffmpeg_local
        
        # Advanced: Cutting
        if start_time and end_time:
            try:
                s = parse_time(start_time)
                e = parse_time(end_time)
                # Define a callback for download_ranges
                def range_func(info_dict, ydl):
                    return [{'start_time': s, 'end_time': e}]
                ydl_opts['download_ranges'] = range_func
                # Force ffmpeg use for cutting (usually required)
                ydl_opts['force_keyframes_at_cuts'] = True 
            except Exception as ex:
                print(f"Time parse error: {ex}")

        # Inject job_id into info_dict for the hook
        def local_hook(d):
            if d['status'] == 'downloading':
                try:
                    p_str = d.get('_percent_str', '0%')
                    # Regex to find number before %
                    match = re.search(r'(\d+\.?\d*)%', p_str)
                    if match:
                        p = float(match.group(1))
                        download_jobs[job_id]['progress'] = p
                except Exception as e:
                    print(f"Progress parse error: {e}")
            elif d['status'] == 'finished':
                download_jobs[job_id]['status'] = 'processing'

        ydl_opts['progress_hooks'] = [local_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Find file
        found_file = None
        for file in os.listdir('.'):
            if file.startswith(filename_base):
                found_file = file
                break
        
        if found_file:
            download_jobs[job_id]['filename'] = found_file
            download_jobs[job_id]['status'] = 'completed'
        else:
            download_jobs[job_id]['status'] = 'error'
            download_jobs[job_id]['error'] = 'File not found'

    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        download_jobs[job_id]['status'] = 'error'
        download_jobs[job_id]['error'] = str(e)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Video Downloader Backend"}

@app.get("/api/public-settings")
def get_public_settings(db: Session = Depends(get_db)):
    """Get public settings (favicon, robots.txt, etc.)"""
    keys = ["favicon_url", "verification_tags", "robots_txt", "site_name", "site_tagline", "analytics_id"]
    settings = db.query(Settings).filter(Settings.key.in_(keys)).all()
    result = {s.key: s.value for s in settings}
    return result

@app.post("/info")
async def get_info(request: UrlRequest):
    try:
        ydl_opts = {'quiet': True, 'nocheckcertificate': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            
            formats_out = []
            formats_out.append({
                'label': 'Audio (MP3/M4A)',
                'quality': 'audio',
                'ext': 'mp3',
                'format_id': 'bestaudio/best',
                'filesize': None
            })

            target_heights = [360, 480, 720, 1080, 2160]
            all_formats = info.get('formats', [])
            
            # Helper to find best video+audio combo
            # We will return specific resolutions (filtered) AND a generic "Best" option
            
            # 1. Add "Best Available" option
            formats_out.append({
                'label': f"Best Quality ({info.get('ext', 'mp4')})",
                'quality': 'best',
                'ext': info.get('ext', 'mp4'),
                'format_id': 'bestvideo+bestaudio/best',
                'filesize': None
            })

            # 2. Try to find specific resolutions, but be more permissive
            # We want to show buttons for any reasonable video format found
            video_formats = {} # height -> format
            
            for f in all_formats:
                height = f.get('height')
                # skip audio-only or invalid
                if not height or f.get('vcodec') == 'none': 
                    continue
                
                # If we haven't seen this height, or this one is better quality (higher tbr/bitrate usually implies better)
                current = video_formats.get(height)
                if not current:
                    video_formats[height] = f
                else:
                    # Prefer mp4 over others if quality is similar
                    if f.get('ext') == 'mp4' and current.get('ext') != 'mp4':
                        video_formats[height] = f
                    # Else prefer higher bitrate
                    elif (f.get('tbr') or 0) > (current.get('tbr') or 0):
                        video_formats[height] = f

            # Add all found video resolutions
            for h in sorted(video_formats.keys()):
                f = video_formats[h]
                
                # Fallback to filesize_approx if filesize is missing
                filesize = f.get('filesize')
                if not filesize:
                    filesize = f.get('filesize_approx')

                formats_out.append({
                    'label': f"{h}p ({f['ext'].upper()})",
                    'quality': f"{h}p",
                    'ext': f['ext'],
                    # Use exact format ID to avoid re-merging if possible, 
                    # but fallback to bestvideo+bestaudio selector logic if strictly needed.
                    # Simple approach: use the format_id directly if it's a single file (not video+audio separate)
                    # BUT yt-dlp often needs merging. 
                    # Safer: request bestvideo[height=X]+bestaudio/best[height=X]
                    'format_id': f"bestvideo[height={h}]+bestaudio/best[height={h}]", 
                    'filesize': filesize
                })

            # Better thumbnail selection
            thumbnail = info.get('thumbnail')
            if not thumbnail and info.get('thumbnails'):
                # Pick the last one (usually highest res)
                thumbnail = info['thumbnails'][-1].get('url')

            return {
                "title": info.get('title'),
                "thumbnail": thumbnail,
                "duration": info.get('duration'),
                "formats": formats_out,
                "webpage_url": info.get('webpage_url') or request.url
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/start_download")
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    download_jobs[job_id] = {
        "status": "pending",
        "progress": 0,
        "filename": None,
        "error": None
    }
    background_tasks.add_task(process_download, job_id, request.url, request.format_id, request.start_time, request.end_time)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = download_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/serve_file/{job_id}")
async def serve_file(job_id: str):
    job = download_jobs.get(job_id)
    if not job or job['status'] != 'completed':
        raise HTTPException(status_code=400, detail="File not ready")
    
    filename = job['filename']
    return FileResponse(
        path=filename,
        filename=f"video_dl_{job_id}{os.path.splitext(filename)[1]}",
        media_type='application/octet-stream',
        background=BackgroundTask(cleanup_file, filename)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
