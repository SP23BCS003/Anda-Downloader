# Deployment Guide for Anda-Downloader

This guide outlines the steps to deploy the Anda-Downloader application. Two deployment options are covered:
1. **Railway (Recommended)** - Quick PaaS deployment
2. **VPS/Linux Server** - Traditional server deployment

---

## 🚀 Railway Deployment (Recommended)

Railway provides a simple, scalable deployment platform with automatic SSL and CI/CD.

### Prerequisites
- GitHub account with your repository
- Railway account (https://railway.app)
- Git installed locally

### Step 1: Prepare Your Repository

Ensure your `.gitignore` excludes:
```
.env
*.db
node_modules/
.venv/
__pycache__/
build/
```

Push all changes to GitHub:
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Deploy Backend Service

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"** → **"Deploy from GitHub Repo"**
3. Select your repository
4. Click **"Add Service"** → **"GitHub Repo"** (same repo)
5. Configure the backend service:
   - Click on the service → **Settings**
   - Set **Root Directory**: `backend`
   - Railway auto-detects Python and uses the `Procfile`

6. Add Environment Variables (Settings → Variables):
   ```
   SECRET_KEY=your-secure-random-string-here
   ```

7. Railway will automatically build and deploy

### Step 3: Deploy Frontend Service

1. Add another service to the same project
2. Click **"Add Service"** → **"GitHub Repo"** (same repo)
3. Configure the frontend service:
   - Set **Root Directory**: `frontend`
   - Set **Build Command**: `npm install && npm run build`
   - Set **Start Command**: `node build/index.js`

4. Get your backend's Railway URL (e.g., `https://backend-xxx.railway.app`)
5. Add Environment Variable:
   ```
   VITE_API_URL=https://your-backend-service.railway.app
   ```

### Step 4: Configure Domain (Optional)

1. In Railway, select your frontend service
2. Go to **Settings** → **Networking** → **Generate Domain**
3. Or add your custom domain

### Step 5: Verify Deployment

1. Open your frontend URL
2. Paste a video URL (e.g., YouTube)
3. Verify video info loads and download works

### Railway Environment Variables Reference

| Service | Variable | Description |
|---------|----------|-------------|
| Backend | `SECRET_KEY` | JWT secret key |
| Backend | `DATABASE_URL` | (Optional) PostgreSQL URL |
| Frontend | `VITE_API_URL` | Backend service URL |

---

## 💻 Traditional VPS Deployment


## 📋 Server Requirements

### Hardware (Minimum)
- **CPU**: 1 Core
- **RAM**: 1 GB (2 GB recommended for build processes)
- **Storage**: 10 GB SSD

### Software Dependencies
You will need to install the following on your server:
- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.10 or newer (3.12 recommended)
- **Node.js**: v18.x or newer
- **Nginx**: Web server and reverse proxy
- **FFmpeg**: Required for video processing
- **Git**: For version control
- **PM2**: Process manager for Node.js (optional but recommended)

---

## 🛠️ Step-by-Step Deployment

### 1. Initial Server Setup

Update your system and install essential packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3-pip python3-venv ffmpeg nginx curl -y
```

### 2. Install Node.js (v18)

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pm2
```

### 3. Clone the Repository

Navigate to your web directory (e.g., `/var/www`) and clone your project:

```bash
cd /var/www
sudo git clone https://github.com/ak7256369/Anda-Downloader.git downloader
sudo chown -R $USER:$USER downloader
cd downloader
```

---

## 🔧 Backend Setup

### 1. Configure Python Environment

Navigate to the backend directory and set up the virtual environment:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Recommended for production
```

### 2. Initialize Database

```bash
python3 init_db.py
```

### 3. Create Systemd Service for Backend

Create a service file to keep the backend running:

```bash
sudo nano /etc/systemd/system/downloader-backend.service
```

Paste the following (adjust paths/user as needed):

```ini
[Unit]
Description=Anda-Downloader Backend
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/downloader/backend
Environment="PATH=/var/www/downloader/backend/.venv/bin"
ExecStart=/var/www/downloader/backend/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

Start the backend:

```bash
sudo systemctl daemon-reload
sudo systemctl start downloader-backend
sudo systemctl enable downloader-backend
```

---

## 🎨 Frontend Setup

### 1. Prepare for Production Build

For a stable VPS deployment, we recommend swapping `adapter-auto` for `adapter-node`.

**On your local machine or server:**

1.  Install the node adapter:
    ```bash
    cd frontend
    npm install -D @sveltejs/adapter-node
    ```

2.  Update `svelte.config.js`:
    ```javascript
    import adapter from '@sveltejs/adapter-node'; // Change from adapter-auto
    // ... rest of file
    ```

### 2. Install and Build

```bash
cd /var/www/downloader/frontend
npm install
npm run build
```

### 3. Run with PM2

Start the Node.js server using PM2 for stability:

```bash
pm2 start build/index.js --name "downloader-frontend" --env PORT=3000
pm2 save
pm2 startup
```

---

## 🌐 Nginx Configuration (Reverse Proxy)

Configure Nginx to serve your frontend and proxy API requests.

```bash
sudo nano /etc/nginx/sites-available/downloader
```

Paste the following configuration:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com; # Replace with your domain

    # Frontend (SvelteKit)
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API (FastAPI)
    location /api/ {
        # You might need to adjust the prefix handling in your FastAPI app 
        # or proxy to / directly if your API structure fits.
        # Assuming FastAPI is mounting /admin etc at root level:
        
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Specific Proxy for Admin/API routes if they are at root level
    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Proxy for other backend endpoints (download, start-download, etc)
    location ~ ^/(download|start-download|favicon.ico) {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/downloader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 SSL Setup (HTTPS)

Secure your site with a free Let's Encrypt certificate:

1.  Install Certbot:
    ```bash
    sudo apt install python3-certbot-nginx
    ```

2.  Obtain Certificate:
    ```bash
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

Certbot will automatically update your Nginx config to force HTTPS.

---

## 🔄 Maintenance

### Updating the App

To deploy a new version:

```bash
cd /var/www/downloader
git pull origin main

# Update Backend
cd backend
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart downloader-backend

# Update Frontend
cd ../frontend
npm install
npm run build
pm2 restart downloader-frontend
```
