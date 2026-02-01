from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from datetime import datetime
from database import Base

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    author = Column(String(100))
    featured_image = Column(String(500))
    status = Column(String(20), default="draft")  # draft, published
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    meta_title = Column(String(200))
    meta_description = Column(String(300))

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text)
    type = Column(String(50))  # string, int, bool, json
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SEOConfig(Base):
    __tablename__ = "seo_config"
    
    id = Column(Integer, primary_key=True, index=True)
    page = Column(String(100), unique=True, index=True, nullable=False)  # home, youtube, tiktok, etc.
    title = Column(String(200))
    description = Column(String(300))
    keywords = Column(Text)
    og_image = Column(String(500))
    structured_data = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
