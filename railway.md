# Anda-Downloader Monorepo

This repository contains two services that should be deployed separately:

## Backend (Python/FastAPI)
- Directory: `backend/`
- Runtime: Python 3.12
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Frontend (Node/SvelteKit)  
- Directory: `frontend/`
- Runtime: Node.js 18
- Build: `npm install && npm run build`
- Start: `node build/index.js`

## Railway Deployment

When deploying to Railway, you must set the **Root Directory** for each service:

1. **Backend Service**: Set Root Directory to `backend`
2. **Frontend Service**: Set Root Directory to `frontend`

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete instructions.
