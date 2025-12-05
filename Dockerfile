
# Use official Python slim image
FROM python:3.11-slim

ENV TZ=UTC
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip cron tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ensure pyotp is installed separately to avoid ModuleNotFound
RUN pip install pyotp

# Copy application code
COPY . .

# Create directories
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Copy cron file
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Set permission + load cron file
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Expose API port
EXPOSE 8080

# Start cron daemon + FastAPI
CMD ["sh", "-c", "cron && uvicorn api:app --host 0.0.0.0 --port 8080"]
