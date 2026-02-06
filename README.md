# Anda-Downloader 🎬

A modern, full-featured video downloader application with admin panel, multi-language support, and mobile-responsive design. Download videos from YouTube, TikTok, Instagram, Facebook, and 10+ other platforms.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-2.0-orange.svg)](https://kit.svelte.dev/)

## ✨ Features

### 🎯 Core Features
- **Multi-Platform Support**: Download from 15+ platforms including YouTube, TikTok, Instagram, Facebook, Twitter, Pinterest, and more
- **High Quality Downloads**: Support for HD, 4K video quality and audio extraction
- **No Watermarks**: Clean downloads without platform watermarks
- **Fast & Free**: No rate limits, completely free to use

### 🌍 Multi-Language Support (i18n)
- **15 Languages Supported**: English, Spanish, French, German, Arabic, Chinese, Hindi, Portuguese, Russian, Japanese, Korean, Italian, Turkish, Vietnamese, Bengali
- **Dynamic Translation**: Entire UI translates instantly
- **Persistent Preferences**: Language selection saved across sessions

### 📱 Mobile Responsive
- **Touch-Optimized UI**: Designed for mobile-first experience
- **Adaptive Layouts**: Separate desktop and mobile layouts
- **Hamburger Menu**: Collapsible navigation for small screens
- **Responsive Components**: All components scale beautifully

### 🔐 Admin Panel
- **Secure Authentication**: JWT-based with SHA256 password hashing
- **Blog Management**: Full CRUD operations for blog posts
- **SEO Manager**: Configure meta tags for all 17 pages
- **Settings Control**: Manage site configuration, analytics, maintenance mode
- **Dashboard**: Real-time statistics and quick actions

### 🎨 Modern Design
- **Beautiful UI**: Premium glassmorphism effects and animations
- **Dark/Light Theme Ready**: Modern color scheme
- **Responsive Design**: Works on all devices
- **Micro-animations**: Smooth transitions and hover effects

### 📋 Additional Features
- **Clipboard Integration**: One-click paste from clipboard
- **Auto-fetch**: Automatically fetches video info on paste
- **Error Handling**: User-friendly error messages
- **Loading States**: Clear feedback during operations

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ak7256369/Anda-Downloader.git
cd Anda-Downloader
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start backend server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. **Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

4. **Access the Application**
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Panel**: http://localhost:5174/admin/login

### Default Admin Credentials
```
Username: admin
Password: admin123
```
⚠️ **IMPORTANT**: Change the default password immediately after first login!

## 📚 Documentation

### Project Structure
```
Anda-Downloader/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # Pydantic models
│   ├── admin_auth.py        # Authentication logic
│   ├── admin_routes.py      # Admin API endpoints
│   ├── init_db.py           # Database initialization
│   ├── requirements.txt     # Python dependencies
│   └── downloader.db        # SQLite database (created after init)
│
└── frontend/
    ├── src/
    │   ├── lib/
    │   │   ├── i18n.ts                  # Internationalization system
    │   │   ├── locales/                 # Translation files (15 languages)
    │   │   └── components/
    │   │       ├── Navbar.svelte        # Navigation with i18n
    │   │       ├── Hero.svelte          # Main downloader UI
    │   │       └── ...
    │   └── routes/
    │       ├── +page.svelte             # Home page
    │       ├── admin/                    # Admin panel routes
    │       │   ├── login/+page.svelte
    │       │   ├── dashboard/+page.svelte
    │       │   ├── blogs/+page.svelte
    │       │   ├── settings/+page.svelte
    │       │   └── seo/+page.svelte
    │       └── [platform]-downloader/    # Platform-specific pages
    └── package.json
```

### Supported Platforms
1. YouTube (Video & MP3)
2. TikTok
3. Instagram (Video, Reels, Stories)
4. Facebook
5. Twitter
6. Pinterest
7. SoundCloud
8. Vimeo
9. Dailymotion
10. Twitch
11. Threads
12. CapCut

### API Endpoints

#### Public
- `POST /download` - Get video information
- `POST /start-download` - Start video download
- `GET /download/{job_id}` - Download video file

#### Admin (Requires Authentication)
- `POST /admin/login` - Admin login
- `GET /admin/stats` - Dashboard statistics
- `GET /admin/blogs` - List all blogs
- `POST /admin/blogs` - Create blog
- `PUT /admin/blogs/{id}` - Update blog
- `DELETE /admin/blogs/{id}` - Delete blog
- `GET /admin/settings` - Get settings
- `PUT /admin/settings` - Update settings
- `GET /admin/seo` - Get all SEO configs
- `PUT /admin/seo/{page}` - Update page SEO

## 🌍 Internationalization (i18n)

### Adding New Languages
1. Create translation file in `frontend/src/lib/locales/{lang_code}.json`
2. Add language to `languages` object in `frontend/src/lib/i18n.ts`
3. Translate all keys following the structure:
```json
{
  "nav": { ... },
  "hero": { ... },
  "errors": { ... }
}
```

### Using Translations in Components
```svelte
<script>
  import { translations, t } from '$lib/i18n';
  $: trans = $translations;
</script>

<h1>{t(trans, 'hero.title')}</h1>
```

## 🔒 Security

### Authentication
- JWT tokens with 24-hour expiration
- SHA256 password hashing with salt
- Secure password verification
- Token stored in localStorage

### Production Recommendations
1. Change `SECRET_KEY` in `admin_auth.py`
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Configure proper CORS origins
5. Add rate limiting
6. Implement CSRF protection
7. Regular security audits

## 🎨 Customization

### Theming
Colors are defined in `frontend/tailwind.config.js`:
```js
colors: {
  primary: '#DC2626',  // Red
  // Add your custom colors
}
```

### SEO Configuration
1. Login to admin panel
2. Navigate to SEO section
3. Configure meta tags for each page
4. Update OpenGraph images

## 🐛 Troubleshooting

### Backend Issues
- **Database not found**: Run `python init_db.py`
- **Port already in use**: Change port in uvicorn command
- **Import errors**: Reinstall dependencies with `pip install -r requirements.txt`

### Frontend Issues
- **Build errors**: Delete `node_modules` and run `npm install` again
- **Translation not working**: Check browser console for import errors
- **Port conflict**: Frontend runs on port 5173 or 5174 automatically

## 📈 Performance

- **Backend**: Async FastAPI for high concurrency
- **Frontend**: SvelteKit for optimal performance
- **Database**: SQLite for development (PostgreSQL recommended for production)
- **Caching**: Ready for Redis integration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [SvelteKit](https://kit.svelte.dev/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling

## 📧 Contact

- **GitHub**: [@ak7256369](https://github.com/ak7256369)
- **Repository**: [Anda-Downloader](https://github.com/ak7256369/Anda-Downloader)

## 🗺️ Roadmap

- [ ] User authentication and download history
- [ ] Batch download support
- [ ] Playlist download functionality
- [ ] Advanced video format options
- [ ] Social sharing features
- [ ] API rate limiting
- [ ] Docker containerization
- [ ] Progressive Web App (PWA)

---

**Made with ❤️ by ak7256369**
