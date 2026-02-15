from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import re

from database import get_db
from models import Admin, Blog, Settings, SEOConfig
from admin_auth import hash_password, verify_password, create_access_token, decode_access_token
import os
import glob
import shutil

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBearer()

# --- Pydantic Models ---

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str

class BlogCreate(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    author: Optional[str] = None
    featured_image: Optional[str] = None
    status: str = "draft"
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    author: Optional[str] = None
    featured_image: Optional[str] = None
    status: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class BlogResponse(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    excerpt: Optional[str]
    author: Optional[str]
    featured_image: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    meta_title: Optional[str]
    meta_description: Optional[str]

    class Config:
        from_attributes = True

class SettingUpdate(BaseModel):
    key: str
    value: str
    type: str = "string"
    description: Optional[str] = None

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    current_password: str

class SEOUpdate(BaseModel):
    page: str
    title: str
    description: str
    keywords: Optional[str] = None
    og_image: Optional[str] = None
    structured_data: Optional[dict] = None

# --- Authentication Dependency ---

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    username = payload.get("sub")
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found or inactive"
        )
    return admin

# --- Helper Functions ---

def create_slug(title: str) -> str:
    """Create URL-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

# --- Routes ---

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Admin login endpoint"""
    admin = db.query(Admin).filter(Admin.username == request.username).first()
        
    if not admin or not verify_password(request.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive"
        )
    
    access_token = create_access_token(data={"sub": admin.username})
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=admin.username
    )


@router.put("/profile")
def update_profile(
    profile: AdminUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Update admin username and password"""
    # Verify current password
    if not verify_password(profile.current_password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    if profile.username:
        # Check if username exists
        existing = db.query(Admin).filter(Admin.username == profile.username, Admin.id != admin.id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        admin.username = profile.username
        
    if profile.password:
        admin.password_hash = hash_password(profile.password)
        
    db.commit()
    db.refresh(admin)
    return {"message": "Profile updated successfully"}

@router.post("/cache/clear")
def clear_cache(
    admin: Admin = Depends(get_current_admin)
):
    """Clear server cache (temporary files)"""
    try:
        from tasks import cleanup_cache
        count = cleanup_cache()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")
        
    return {"message": f"Cache cleared successfully. Removed {count} items."}

# --- Blog Routes ---

@router.get("/blogs", response_model=List[BlogResponse])
def get_blogs(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Get all blogs (admin only)"""
    query = db.query(Blog)
    if status:
        query = query.filter(Blog.status == status)
    blogs = query.order_by(Blog.created_at.desc()).offset(skip).limit(limit).all()
    return blogs

@router.get("/blogs/{blog_id}", response_model=BlogResponse)
def get_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Get a single blog by ID"""
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.post("/blogs", response_model=BlogResponse)
def create_blog(
    blog: BlogCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Create a new blog post"""
    slug = create_slug(blog.title)
    
    # Check if slug exists
    existing = db.query(Blog).filter(Blog.slug == slug).first()
    if existing:
        slug = f"{slug}-{datetime.utcnow().timestamp()}"
    
    db_blog = Blog(
        title=blog.title,
        slug=slug,
        content=blog.content,
        excerpt=blog.excerpt,
        author=blog.author or admin.username,
        featured_image=blog.featured_image,
        status=blog.status,
        meta_title=blog.meta_title or blog.title,
        meta_description=blog.meta_description or blog.excerpt
    )
    
    if blog.status == "published":
        db_blog.published_at = datetime.utcnow()
    
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

@router.put("/blogs/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Update an existing blog post"""
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    update_data = blog.dict(exclude_unset=True)
    
    # If title changed, update slug
    if "title" in update_data:
        new_slug = create_slug(update_data["title"])
        if new_slug != db_blog.slug:
            existing = db.query(Blog).filter(Blog.slug == new_slug, Blog.id != blog_id).first()
            if not existing:
                db_blog.slug = new_slug
    
    # Set published_at if status changed to published
    if update_data.get("status") == "published" and db_blog.status != "published":
        db_blog.published_at = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(db_blog, key, value)
    
    db.commit()
    db.refresh(db_blog)
    return db_blog

@router.delete("/blogs/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Delete a blog post"""
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}

# --- Settings Routes ---

@router.get("/settings")
def get_settings(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Get all settings"""
    settings = db.query(Settings).all()
    return {s.key: {"value": s.value, "type": s.type, "description": s.description} for s in settings}

@router.put("/settings")
def update_settings(
    settings: List[SettingUpdate],
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Update multiple settings"""
    for setting in settings:
        db_setting = db.query(Settings).filter(Settings.key == setting.key).first()
        if db_setting:
            db_setting.value = setting.value
            db_setting.type = setting.type
            if setting.description:
                db_setting.description = setting.description
        else:
            db_setting = Settings(
                key=setting.key,
                value=setting.value,
                type=setting.type,
                description=setting.description
            )
            db.add(db_setting)
    
    db.commit()
    return {"message": "Settings updated successfully"}

# --- SEO Routes ---

@router.get("/seo")
def get_seo_configs(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Get all SEO configurations"""
    configs = db.query(SEOConfig).all()
    return {c.page: {
        "title": c.title,
        "description": c.description,
        "keywords": c.keywords,
        "og_image": c.og_image,
        "structured_data": c.structured_data
    } for c in configs}

@router.put("/seo/{page}")
def update_seo(
    page: str,
    seo: SEOUpdate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Update SEO configuration for a specific page"""
    db_seo = db.query(SEOConfig).filter(SEOConfig.page == page).first()
    if db_seo:
        db_seo.title = seo.title
        db_seo.description = seo.description
        db_seo.keywords = seo.keywords
        db_seo.og_image = seo.og_image
        db_seo.structured_data = seo.structured_data
    else:
        db_seo = SEOConfig(**seo.dict())
        db.add(db_seo)
    
    db.commit()
    db.refresh(db_seo)
    return {"message": "SEO configuration updated"}

# --- Dashboard Stats ---

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):
    """Get dashboard statistics"""
    total_blogs = db.query(Blog).count()
    published_blogs = db.query(Blog).filter(Blog.status == "published").count()
    draft_blogs = db.query(Blog).filter(Blog.status == "draft").count()
    
    return {
        "total_blogs": total_blogs,
        "published_blogs": published_blogs,
        "draft_blogs": draft_blogs,
        "total_admins": db.query(Admin).count()
    }

@router.post("/system/update-ytdlp")
def trigger_update_ytdlp(
    admin: Admin = Depends(get_current_admin)
):
    """Manually trigger yt-dlp update"""
    try:
        from manual_update import update_ytdlp
        # Run in a separate process or thread would be better for long tasks, 
        # but for simplicity and immediate feedback we run it here.
        # However, since it installs packages, it might kill the worker if it restarts python.
        # Actually, in a container, pip install might not immediately affect the running process 
        # unless we reload. But for yt-dlp (CLI tool), it should work for next subprocess call.
        
        import subprocess
        import sys
        
        # We run the script as a subprocess to capture output cleanly
        result = subprocess.check_output(
            [sys.executable, "manual_update.py"], 
            stderr=subprocess.STDOUT,
            text=True
        )
        return {"message": "Update completed successfully", "log": result}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {e.output}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
