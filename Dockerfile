# ==========================
# 1) BUILDER STAGE
# ==========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ==========================
# 2) RUNTIME STAGE
# ==========================
FROM python:3.11-slim

# Set timezone UTC
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Create volume directories
RUN mkdir -p /data /cron

# Copy python dependencies from builder
COPY --from=builder /usr/local /usr/local

# Copy entire project
COPY . /app
RUN ls -R /app


# Permissions
RUN chmod +x /app/app/cron_job.sh
RUN chmod 644 /app/app/totp.cron

# Register cron job
RUN crontab -r || true
RUN crontab /app/app/totp.cron


# Expose API port
EXPOSE 8080

# Start cron + FastAPI server
CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
