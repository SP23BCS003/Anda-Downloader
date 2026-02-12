"""
Database initialization script
Creates default admin user and initial settings
"""
from database import engine, SessionLocal, init_db
from models import Admin, Settings, SEOConfig, Base
from admin_auth import hash_password

def create_default_data():
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not admin:
            print("Creating default admin user...")
            admin = Admin(
                username="admin",
                password_hash=hash_password("admin123"),  # Change this password!
                email="admin@example.com",
                is_active=True
            )
            db.add(admin)
            print("[OK] Default admin created: username='admin', password='admin123'")
            print("[WARN]  IMPORTANT: Change the default password after first login!")
        else:
            # Force reset password if admin exists (for recovery)
            print("Admin user found. verifying/resetting default password...")
            admin.password_hash = hash_password("admin123")
            db.add(admin) # Ensure it's tracked
            print("[OK] Admin password reset to 'admin123'")
        
        # Create default settings
        default_settings = [
            ("site_name", "Anda-Downloader", "string", "Website name"),
            ("site_tagline", "Download videos from any platform", "string", "Website tagline"),
            ("contact_email", "contact@example.com", "string", "Contact email address"),
            ("default_language", "en", "string", "Default language code"),
            ("maintenance_mode", "false", "bool", "Enable maintenance mode"),
            ("analytics_id", "", "string", "Google Analytics tracking ID"),
        ]
        
        for key, value, type_, desc in default_settings:
            setting = db.query(Settings).filter(Settings.key == key).first()
            if not setting:
                setting = Settings(key=key, value=value, type=type_, description=desc)
                db.add(setting)
        
        print("[OK] Default settings created")
        
        # Create default SEO configurations
        seo_pages = [
            # Main pages
            ("home", "Free Online Video Downloader - Download Videos from Any Site", 
             "Download videos from YouTube, TikTok, Instagram, Facebook, Twitter and more. Fast, free, and easy video downloader for all platforms.",
             "video downloader, download videos, youtube downloader, tiktok downloader, instagram downloader",
             ""),
            
            # Video downloaders
            ("youtube-downloader", "YouTube Video Downloader - Download YouTube Videos Free",
             "Download YouTube videos in HD quality. Fast and free YouTube downloader with multiple format options.",
             "youtube downloader, download youtube videos, youtube to mp4, youtube video download",
             ""),
            ("youtube-to-mp3", "YouTube to MP3 Converter - Download YouTube Audio",
             "Convert YouTube videos to MP3 audio format. High quality audio extraction from YouTube videos.",
             "youtube to mp3, youtube converter, youtube audio download, youtube mp3",
             ""),
            ("tiktok-downloader", "TikTok Video Downloader - Download TikTok Without Watermark",
             "Download TikTok videos without watermark. Save TikTok videos in HD quality for free.",
             "tiktok downloader, download tiktok videos, tiktok no watermark, save tiktok",
             ""),
            ("instagram-downloader", "Instagram Video Downloader - Download Instagram Reels & Stories",
             "Download Instagram videos, reels, and stories. Save Instagram content in high quality.",
             "instagram downloader, download instagram videos, instagram reels download, save instagram",
             ""),
            ("facebook-downloader", "Facebook Video Downloader - Download FB Videos Free",
             "Download Facebook videos in HD. Save videos from Facebook to your device for free.",
             "facebook downloader, download facebook videos, fb video download, save facebook video",
             ""),
            ("twitter-downloader", "Twitter Video Downloader - Download Twitter Videos & GIFs",
             "Download Twitter videos and GIFs. Save tweets with videos in high quality.",
             "twitter downloader, download twitter videos, save twitter video, twitter video download",
             ""),
            ("vimeo-downloader", "Vimeo Video Downloader - Download Vimeo Videos Free",
             "Download Vimeo videos in HD quality. Free Vimeo video downloader.",
             "vimeo downloader, download vimeo videos, vimeo video download",
             ""),
            ("dailymotion-downloader", "Dailymotion Video Downloader - Download Dailymotion Videos",
             "Download Dailymotion videos for free. Save Dailymotion content in high quality.",
             "dailymotion downloader, download dailymotion videos, dailymotion video download",
             ""),
            ("twitch-downloader", "Twitch Video Downloader - Download Twitch Clips & VODs",
             "Download Twitch clips and VODs. Save your favorite Twitch moments.",
             "twitch downloader, download twitch clips, twitch vod download, save twitch video",
             ""),
            ("twitch-downloader", "Twitch Video Downloader - Download Twitch Clips & VODs",
             "Download Twitch clips and VODs. Save your favorite Twitch moments.",
             "twitch downloader, download twitch clips, twitch vod download, save twitch video",
             ""),
            
            # Audio downloader
            ("soundcloud-downloader", "SoundCloud Downloader - Download SoundCloud Music Free",
             "Download SoundCloud tracks and playlists. Free SoundCloud music downloader.",
             "soundcloud downloader, download soundcloud music, soundcloud mp3 download",
             ""),
            
            # Other pages
            ("contact", "Contact Us - Anda Downloader",
             "Get in touch with us. Contact Anda Downloader for support and inquiries.",
             "contact, support, help",
             ""),
            ("privacy", "Privacy Policy - Anda Downloader",
             "Read our privacy policy to understand how we protect your data.",
             "privacy policy, data protection, privacy",
             ""),
            ("terms", "Terms of Service - Anda Downloader",
             "Terms and conditions for using Anda Downloader service.",
             "terms of service, terms and conditions, legal",
             ""),
        ]
        
        for page, title, desc, keywords, og_img in seo_pages:
            seo = db.query(SEOConfig).filter(SEOConfig.page == page).first()
            if not seo:
                seo = SEOConfig(
                    page=page,
                    title=title,
                    description=desc,
                    keywords=keywords,
                    og_image=og_img
                )
                db.add(seo)
        
        print("[OK] Default SEO configurations created")
        
        db.commit()
        print("\n[OK] Database initialized successfully!")
        
    except Exception as e:
        print(f"[ERROR] Error initializing database: {e}")
        db.rollback()
        raise e  # Re-raise to let caller know
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    create_default_data()
