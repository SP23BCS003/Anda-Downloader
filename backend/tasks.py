import os
import glob
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_cache():
    """
    Clear server cache (temporary files, downloads, pycache).
    Returns the count of removed items.
    """
    count = 0
    errors = 0
    
    logger.info("Starting cache cleanup...")
    
    try:
        # 1. Clear temp files in root (temp_*)
        for f in glob.glob("temp_*"):
            try:
                os.remove(f)
                count += 1
            except Exception as e:
                logger.error(f"Error removing {f}: {e}")
                errors += 1
            
        # 2. Clear downloads folder content
        for f in glob.glob("downloads/*"):
            try:
                if os.path.isfile(f):
                    os.remove(f)
                elif os.path.isdir(f):
                    shutil.rmtree(f)
                count += 1
            except Exception as e:
                logger.error(f"Error removing {f}: {e}")
                errors += 1
            
        # 3. Clear __pycache__ directories recursively
        for f in glob.glob("**/__pycache__", recursive=True):
            try:
                shutil.rmtree(f)
                count += 1
            except Exception as e:
                logger.error(f"Error removing {f}: {e}")
                errors += 1
                
        logger.info(f"Cache cleanup completed. Removed {count} items. Errors: {errors}")
        return count
        
    except Exception as e:
        logger.error(f"Detailed cache cleanup failed: {e}")
        return 0
