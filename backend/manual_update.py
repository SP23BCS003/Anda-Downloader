import subprocess
import sys

def update_ytdlp():
    print("Starting manual update of yt-dlp...")
    try:
        # Check current version
        try:
            current_ver = subprocess.check_output(["yt-dlp", "--version"], text=True).strip()
            print(f"Current version: {current_ver}")
        except:
            print("Current version: Unknown")

        # Uninstall existing
        print("Uninstalling current yt-dlp...")
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "yt-dlp"])
        
        # Install from master
        print("Installing yt-dlp from git master...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "git+https://github.com/yt-dlp/yt-dlp.git@master",
            "--upgrade",
            "--force-reinstall",
            "--no-cache-dir"
        ])
        
        # Verify version
        print("Verifying installation...")
        result = subprocess.check_output(["yt-dlp", "--version"], text=True)
        print(f"SUCCESS: yt-dlp updated to version {result.strip()}")
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Update failed with code {e.returncode}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    update_ytdlp()
