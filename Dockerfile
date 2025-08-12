FROM python:3.13 AS builder

# Copy UV binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Environment variables for build optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=never \
  UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# Install Python dependencies (separate layer for better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project

# Copy source code and install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-editable

FROM python:3.13-slim AS runtime

# Install runtime dependencies in a single layer
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  libpq5 \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user and directories in one layer
RUN adduser --disabled-password --gecos "" --uid 1000 appuser && \
  mkdir -p /app/data && \
  chown appuser:appuser /app

# Set working directory and user
WORKDIR /app
USER appuser

# Copy application files with correct ownership
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app /app

# Runtime environment
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/app/.venv/bin:$PATH"

# Health check for container monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD python -c "import django; print('OK')" || exit 1

# Default port exposure
EXPOSE 8000
