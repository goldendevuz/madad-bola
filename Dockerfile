# === Stage 1: builder ===
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl sudo make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# === Stage 2: final runtime image ===
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install make (needed for start.sh)
RUN apt-get update && apt-get install -y --no-install-recommends make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/pip /usr/local/bin/pip

# Also copy all executables installed via pip (like gunicorn)
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

EXPOSE 1025

CMD ["bash", "start.sh"]
