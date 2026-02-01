
import os
import zipfile
import urllib.request
import shutil
import ssl
import sys
import time

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
ZIP_PATH = "ffmpeg_antigravity.zip"
DEST_DIR = "ffmpeg_antigravity_temp"
FINAL_DIR = "ffmpeg"

def report_progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = downloaded * 100 / total_size
        sys.stdout.write(f"\rDownloading: {percent:.2f}% ({downloaded / (1024*1024):.1f} MB)")
    else:
        sys.stdout.write(f"\rDownloading: {downloaded / (1024*1024):.1f} MB")
    sys.stdout.flush()

def download_ffmpeg():
    print(f"Downloading FFmpeg from {FFMPEG_URL}...")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # User-Agent header
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
    urllib.request.install_opener(opener)

    try:
        urllib.request.urlretrieve(FFMPEG_URL, ZIP_PATH, reporthook=report_progress)
        print("\nDownload complete.")
    except Exception as e:
        print(f"\nFailed to download: {e}")
        return False
    return True

def install():
    if os.path.exists(FINAL_DIR):
        if os.path.exists(os.path.join(FINAL_DIR, 'ffmpeg.exe')):
            print("FFmpeg already installed.")
            return

    # Check zip
    valid_zip = False
    if os.path.exists(ZIP_PATH):
        print("Checking existing zip file...")
        try:
            with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
                if zip_ref.testzip() is None:
                    valid_zip = True
                    print("Existing zip is valid.")
                else:
                    print("Existing zip is corrupt.")
        except zipfile.BadZipFile:
            print("Existing zip is bad.")
        except Exception as e:
            print(f"Error checking zip: {e}")
    
    if not valid_zip:
        if not download_ffmpeg():
            return

    print("Extracting...")
    try:
        if os.path.exists(DEST_DIR):
            shutil.rmtree(DEST_DIR)
        
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(DEST_DIR)
            
        # Find bin folder
        bin_path = None
        for root, dirs, files in os.walk(DEST_DIR):
            if 'bin' in dirs:
                bin_path = os.path.join(root, 'bin')
                break
        
        if not bin_path:
            print("Could not find bin folder in extracted files.")
            return

        if not os.path.exists(FINAL_DIR):
            os.makedirs(FINAL_DIR)

        for file in ['ffmpeg.exe', 'ffprobe.exe']:
            src = os.path.join(bin_path, file)
            dst = os.path.join(FINAL_DIR, file)
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"Moved {file} to {FINAL_DIR}")
            else:
                print(f"Warning: {file} not found in bin")

        print("Cleaning up...")
        if os.path.exists(ZIP_PATH):
            os.remove(ZIP_PATH)
        if os.path.exists(DEST_DIR):
            shutil.rmtree(DEST_DIR)

        print("SUCCESS: FFmpeg installed.")
        
    except Exception as e:
        print(f"Installation failed: {e}")

if __name__ == "__main__":
    install()
