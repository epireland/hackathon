# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    sqlite3 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH (installed to /root/.local/bin)
ENV PATH="/root/.local/bin:$PATH"

# Copy pyproject.toml and source code
COPY pyproject.toml .
COPY src/ ./src/
COPY app.py .

# Install the application and its dependencies using uv
# Use --no-cache to ensure fresh install and avoid binary compatibility issues
RUN uv pip install --no-cache -e .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set database path to persistent volume
ENV DB_PATH=/app/data/shift_handover.db

# Expose Streamlit default port
EXPOSE 8501

# Health check - using wget instead of requests to avoid extra dependency
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
