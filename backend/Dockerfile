# --- Stage 1: Build stage with all dependencies ---
FROM python:3.13-alpine3.21 AS builder
LABEL maintainer="xuzmonomi.com"

# Build argument for dev dependencies
ARG DEV=false

# Install build-time dependencies, including libstdc++
RUN apk add --no-cache \
        postgresql-client \
        libstdc++ \
        libgcc \
        freetype \
        fontconfig \
        ttf-dejavu \
        jpeg \
        libjpeg \
        libpng \
    && apk add --no-cache --virtual .tmp-build-deps \
        build-base \
        postgresql-dev \
        musl-dev \
        zlib \
        zlib-dev \
        linux-headers \
        libffi-dev \
        openssl-dev \
        jpeg-dev \
        libpng-dev \
        freetype-dev \
        lcms2-dev \
        tiff-dev

RUN mkdir /app     
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt

# Install Python dependencies into a virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --no-cache-dir --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install --no-cache-dir -r /tmp/requirements.dev.txt; \
    fi && \
    # Clean up temporary build dependencies
    apk del .tmp-build-deps

# --- Stage 2: Final lightweight runtime stage ---
FROM python:3.13-alpine3.21

# Headless + unbuffered Python output for logs
ENV PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg 
    
# Copy the virtual environment and installed packages from the builder stage
COPY --from=builder /py /py

# Set working directory before copying application code
WORKDIR /app

# Copy application code into /app
COPY . /app

EXPOSE 8000

# Install minimal runtime dependencies needed for the application
RUN apk add --no-cache \
        postgresql-client \
        libstdc++ \
        libgcc \
        freetype \
        fontconfig \
        ttf-dejavu \
        jpeg \
        libjpeg \
        libpng \
        lcms2 \
        tiff

# Set up user and permissions
RUN adduser --disabled-password --home /home/app-user app-user && \
    mkdir -p /vol/web/media /vol/web/static /tmp/.cache/matplotlib /scripts && \
    chown -R app-user:app-user /vol /tmp/.cache/matplotlib /home/app-user /scripts /app && \
    chmod -R 755 /vol /scripts /app && \
    chmod +x /app/scripts/run.sh

ENV PATH="/app/scripts:/py/bin:$PATH"

USER app-user

CMD ["/app/scripts/run.sh"]