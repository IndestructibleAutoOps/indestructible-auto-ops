# GL30-49 Execution Layer - Docker Image
FROM python:3.11-slim

LABEL maintainer="gl-engine-team@machinenativeops.io"
LABEL version="1.0.0"
LABEL description="GL Execution Engine for Machine Native Ops"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    yamllint \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scripts/gl-engine/ /app/scripts/gl-engine/
COPY tests/ /app/tests/
COPY gl/ /app/gl/

# Create directories
RUN mkdir -p /app/logs /app/reports /app/artifacts

# Set environment variables
ENV PYTHONPATH=/app
ENV GL_ENGINE_LOG_LEVEL=INFO
ENV GL_ENGINE_LOG_DIR=/app/logs
ENV GL_ENGINE_REPORT_DIR=/app/reports
ENV GL_ENGINE_ARTIFACT_DIR=/app/artifacts

# Create non-root user
RUN useradd -m -u 1000 gluser && \
    chown -R gluser:gluser /app

# Switch to non-root user
USER gluser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from scripts.gl_engine.gl_executor import GLLayerExecutor; executor = GLLayerExecutor(); print('OK')" || exit 1

# Default command
CMD ["python", "-m", "scripts.gl_engine.gl_executor"]