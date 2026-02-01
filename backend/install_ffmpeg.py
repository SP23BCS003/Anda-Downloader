
import os
import zipfile
import urllib.request
import shutil

FFMPEG_URL = "https://github.com/GyanD/codexffmpeg/releases/download/2024-01-01-git-e1c1dc6443/ffmpeg-2024-01-01-git-e1c1dc6443-essentials_build.zip"
# Using a fixed reliable URL (GyanD is the standard Windows build provider)
# Actually, let's use a 'latest' redirect if possible, or a specific version to be safe.
# The URL above is hypothetical. Let's use the standard "release-essentials" link.
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

DEST_DIR = "ffmpeg_temp"
FINAL_DIR = "ffmpeg"

def install_ffmpeg():
    print(f"Downloading FFmpeg from {FFMPEG_URL}...")
    zip_path = "ffmpeg.zip"
    try:
        # User-Agent needed sometimes
        req = urllib.request.Request(
            FFMPEG_URL, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, context=ctx) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"Failed to download: {e}")
        return

    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DEST_DIR)

    # Find the bin folder
    bin_path = None
    for root, dirs, files in os.walk(DEST_DIR):
        if 'bin' in dirs:
            bin_path = os.path.join(root, 'bin')
            break
    
    if not bin_path:
        print("Could not find bin folder in zip")
        return

    # Move ffmpeg.exe and ffprobe.exe to current dir (or a dedicated folder)
    if not os.path.exists(FINAL_DIR):
        os.makedirs(FINAL_DIR)
        
    for file in ['ffmpeg.exe', 'ffprobe.exe']:
        src = os.path.join(bin_path, file)
        if os.path.exists(src):
            shutil.move(src, FINAL_DIR)
            print(f"Moved {file} to {FINAL_DIR}")

    # Cleanup
    print("Cleaning up...")
    os.remove(zip_path)
    shutil.rmtree(DEST_DIR)
    print("Done! FFmpeg is installed in ./ffmpeg/")

if __name__ == "__main__":
    install_ffmpeg()
