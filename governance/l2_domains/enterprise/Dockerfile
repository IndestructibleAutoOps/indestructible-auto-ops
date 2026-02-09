# Enterprise Governance Framework - Multi-stage Dockerfile
# Supports both Python and Node.js components

# ============================================
# Stage 1: Python Base
# ============================================
FROM python:3.11-slim as python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# ============================================
# Stage 2: Node.js Base
# ============================================
FROM node:20-alpine as node-base

# Set working directory
WORKDIR /app

# ============================================
# Stage 3: Python Dependencies
# ============================================
FROM python-base as python-deps

# Copy requirements
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .[dev]

# ============================================
# Stage 4: Node.js Dependencies
# ============================================
FROM node-base as node-deps

# Copy package files
COPY package*.json ./

# Install Node.js dependencies
RUN npm ci --only=production

# ============================================
# Stage 5: Python Runtime
# ============================================
FROM python-base as python-runtime

# Copy dependencies from python-deps
COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY configs/ ./configs/

# Create necessary directories
RUN mkdir -p /app/data/evidence \
    /app/data/events \
    /app/data/migrations \
    /app/logs \
    /app/reports

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose ports
EXPOSE 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ============================================
# Stage 6: Development Image
# ============================================
FROM python-runtime as development

# Switch to root user for development
USER root

# Install additional dev tools
RUN pip install pytest pytest-cov black ruff mypy

# Copy development files
COPY tests/ ./tests/
COPY Makefile ./
COPY .env.example ./

# Switch back to appuser
USER appuser

# Default command for development
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Stage 7: Production Image
# ============================================
FROM python-runtime as production

# Optimization: remove unnecessary files
RUN find /usr/local/lib/python3.11/site-packages -name '*.pyc' -delete && \
    find /usr/local/lib/python3.11/site-packages -name '*.pyo' -delete && \
    find /usr/local/lib/python3.11/site-packages -type d -name '__pycache__' -exec rm -rf {} +

# Production command with multiple workers
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]