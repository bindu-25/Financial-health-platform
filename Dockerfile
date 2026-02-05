FROM python:3.11.8-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System deps for pandas/numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (cache-friendly)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Railway uses port 8080
EXPOSE 8080

# Start server
CMD ["gunicorn", "backend_app:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
