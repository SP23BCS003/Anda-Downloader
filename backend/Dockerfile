FROM python:3.11-slim

# Install ffmpeg and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify ffmpeg is installed
RUN ffmpeg -version

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt && \
    pip install --no-cache-dir --upgrade "yt-dlp>=2024.11.04"

# Copy application code
COPY . .

# Create downloads directory
RUN mkdir -p downloads

# Default port (Railway overrides via $PORT env var)
ENV PORT=8000
EXPOSE ${PORT}

# Start the application (shell form to expand $PORT)
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
