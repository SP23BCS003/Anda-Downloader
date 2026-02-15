from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Blog, Settings, SEOConfig

router = APIRouter(tags=["public"])

# --- Blog Public Routes ---

@router.get("/api/blogs")
def get_public_blogs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get published blogs for frontend"""
    blogs = db.query(Blog).filter(Blog.status == "published") \
        .order_by(Blog.published_at.desc()) \
        .offset(skip).limit(limit).all()
    return blogs

@router.get("/api/blogs/{slug}")
def get_public_blog(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get single published blog by slug"""
    blog = db.query(Blog).filter(Blog.slug == slug, Blog.status == "published").first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

# --- Sitemap Routes ---

@router.get("/sitemap.xml")
def sitemap_xml(request: Request, db: Session = Depends(get_db)):
    """Generate XML Sitemap"""
    base_url = str(request.base_url).rstrip("/")
    
    # 1. Static Pages
    mod_date = datetime.now().strftime("%Y-%m-%d")
    pages = [
        "",
        "/youtube-downloader",
        "/facebook-downloader",
        "/instagram-downloader",
        "/tiktok-downloader",
        "/twitter-downloader",
        "/twitch-downloader",
        "/vimeo-downloader",
        "/soundcloud-downloader",
        "/dailymotion-downloader",
        "/youtube-to-mp3",
        "/contact",
        "/privacy",
        "/terms",
        "/blogs"
    ]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for p in pages:
        xml.append(f"""
    <url>
        <loc>{base_url}{p}</loc>
        <lastmod>{mod_date}</lastmod>
        <changefreq>daily</changefreq>
        <priority>0.8</priority>
    </url>""")
        
    # 2. Blog Posts
    blogs = db.query(Blog).filter(Blog.status == "published").all()
    for blog in blogs:
        date = blog.updated_at.strftime("%Y-%m-%d") if blog.updated_at else mod_date
        xml.append(f"""
    <url>
        <loc>{base_url}/blogs/{blog.slug}</loc>
        <lastmod>{date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.6</priority>
    </url>""")
        
    xml.append('</urlset>')
    
    return Response(content="\n".join(xml), media_type="application/xml")

@router.get("/sitemap.html", response_class=HTMLResponse)
def sitemap_html(request: Request, db: Session = Depends(get_db)):
    """Generate HTML Sitemap"""
    base_url = str(request.base_url).rstrip("/")
    
    # Static Pages
    pages = [
        ("Home", "/"),
        ("YouTube Downloader", "/youtube-downloader"),
        ("Facebook Downloader", "/facebook-downloader"),
        ("Instagram Downloader", "/instagram-downloader"),
        ("TikTok Downloader", "/tiktok-downloader"),
        ("Twitter Downloader", "/twitter-downloader"),
        ("Twitch Downloader", "/twitch-downloader"),
        ("Vimeo Downloader", "/vimeo-downloader"),
        ("SoundCloud Downloader", "/soundcloud-downloader"),
        ("Dailymotion Downloader", "/dailymotion-downloader"),
        ("YouTube to MP3", "/youtube-to-mp3"),
        ("Blogs", "/blogs"),
        ("Contact", "/contact"),
        ("Privacy Policy", "/privacy"),
        ("Terms of Service", "/terms"),
    ]
    
    # Blog Posts
    blogs = db.query(Blog).filter(Blog.status == "published").order_by(Blog.published_at.desc()).all()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sitemap - Anda-Downloader</title>
        <style>
            body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; color: #333; }}
            h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            h2 {{ margin-top: 30px; color: #dc2626; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 8px; }}
            a {{ text-decoration: none; color: #2563eb; }}
            a:hover {{ text-decoration: underline; }}
            .date {{ color: #666; font-size: 0.9em; margin-left: 10px; }}
        </style>
    </head>
    <body>
        <h1>Sitemap</h1>
        
        <h2>Pages</h2>
        <ul>
            {''.join([f'<li><a href="{base_url}{path}">{name}</a></li>' for name, path in pages])}
        </ul>
        
        <h2>Latest Blog Posts</h2>
        <ul>
            {''.join([f'<li><a href="{base_url}/blogs/{b.slug}">{b.title}</a> <span class="date">{b.published_at.strftime("%b %d, %Y") if b.published_at else ""}</span></li>' for b in blogs])}
        </ul>
        
        <p style="margin-top: 50px; text-align: center; color: #888; font-size: 0.9em;">
            &copy; {datetime.now().year} Anda-Downloader. All rights reserved.
        </p>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)
