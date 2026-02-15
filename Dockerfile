# Multi-stage build: Frontend + Backend
FROM node:18-alpine AS frontend-build

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend_app.py .
COPY src/ ./src/
COPY config/ ./config/

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting FinSight AI..."\n\
uvicorn backend_app:app --host 0.0.0.0 --port ${PORT:-8000}\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run application
CMD ["/app/start.sh"]
