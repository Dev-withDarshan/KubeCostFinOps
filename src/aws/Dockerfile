# ==============================================================================
# Multi-Stage Production Dockerfile for KubeCostFinOps Intelligence Platform
# 
# Security Standards:
# - Minimal attack surface based on python:3.11-slim
# - Non-root unprivileged service execution (UID 10001: finops)
# - Zero pip/compiler overhead in final runtime stage
# - Built-in container healthcheck via standard library
# ==============================================================================

FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies if required (standard library architecture requires no extra pip packages)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt || true

# ------------------------------------------------------------------------------
# Final Runtime Container
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runner

# Create non-root system user and group
RUN groupadd -g 10001 finops && \
    useradd -u 10001 -g finops -s /bin/sh -m finops

WORKDIR /app

# Copy application source code and artifacts
COPY src/ /app/src/
COPY results/ /app/results/
COPY scripts/ /app/scripts/
COPY README.md /app/README.md

# Set ownership to unprivileged user
RUN chown -R finops:finops /app

USER finops:finops

# Expose standard REST API and Dashboard port
EXPOSE 8000

# Configure environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health')" || exit 1

# Launch Python FinOps API Server and Web Dashboard
ENTRYPOINT ["python", "-m", "src.backend.main"]
CMD ["--host", "0.0.0.0", "--port", "8000", "--results-dir", "results"]
