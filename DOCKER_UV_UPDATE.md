# Docker Update: UV Package Manager Integration

## Summary

The Dockerfile has been updated to use **uv** (ultrafast Python package installer) instead of pip, with dependencies managed through `pyproject.toml` instead of `requirements.txt`.

## Changes Made

### 1. **Dockerfile Updates**

#### Before (using pip + requirements.txt):
```dockerfile
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
```

#### After (using uv + pyproject.toml):
```dockerfile
# Install system dependencies and uv
RUN apt-get update && apt-get install -y \
    sqlite3 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy pyproject.toml and source code
COPY pyproject.toml .
COPY src/ ./src/
COPY app.py .

# Install the application and its dependencies using uv
RUN uv pip install -e .
```

### 2. **Environment Variables**
Added `UV_SYSTEM_PYTHON=1` to tell uv to use the system Python installation.

### 3. **System Dependencies**
Added `curl` to the system dependencies to download and install uv.

### 4. **pyproject.toml Updates**
Updated the package configuration:
```toml
[tool.hatch.build.targets.wheel]
packages = ["src"]  # Changed from ["database", "pages", "utils"]
```

### 5. **.dockerignore Updates**
Removed `pyproject.toml` from the ignore list to ensure it's included in the Docker build.

### 6. **Documentation Updates**
- Updated `DOCKER.md` to mention uv as the package manager
- Updated `DOCKER_SETUP.md` to reflect uv usage in image layers

## Benefits of Using UV

1. **Speed**: uv is significantly faster than pip for dependency resolution and installation
2. **Consistency**: Same package manager used in development and production
3. **Modern**: Uses pyproject.toml standard instead of requirements.txt
4. **Reliability**: Better dependency resolution and conflict detection

## Build & Deploy

The build and deployment commands remain the same:

### Using Docker Compose:
```bash
docker-compose up -d
```

### Using Build Scripts:
```bash
# Windows
docker-build.bat

# Linux/Mac
./docker-build.sh
```

### Manual Build:
```bash
docker build -t shift-handover:latest .
docker run -d -p 8501:8501 -v shift-handover-data:/app/data shift-handover:latest
```

## Verification

The Docker image now:
- ✅ Uses Python 3.11
- ✅ Installs uv package manager
- ✅ Reads dependencies from `pyproject.toml`
- ✅ Installs application in editable mode
- ✅ Maintains database persistence via volumes
- ✅ Includes health checks
- ✅ Optimized for production use

## Testing the Updated Docker Image

1. **Build the image:**
   ```bash
   docker build -t shift-handover:latest .
   ```

2. **Verify uv is installed:**
   ```bash
   docker run --rm shift-handover:latest uv --version
   ```

3. **Check installed packages:**
   ```bash
   docker run --rm shift-handover:latest uv pip list
   ```

4. **Run the application:**
   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

5. **Access the app:**
   Navigate to `http://localhost:8501`

## Troubleshooting

### Issue: uv installation fails
**Solution**: Ensure internet connectivity during build. The Dockerfile downloads uv installer from astral.sh.

### Issue: Dependencies not found
**Solution**: Verify `pyproject.toml` is not in `.dockerignore` and contains correct dependencies.

### Issue: Import errors
**Solution**: Ensure the package structure in `pyproject.toml` matches actual directory structure (should be `["src"]`).

## Migration Notes

- **requirements.txt is no longer used** in the Docker build
- All dependencies should be defined in `pyproject.toml`
- The editable install (`-e .`) allows for easier debugging if needed
- Docker layer caching is optimized by installing dependencies with source code

## Next Steps

- ✅ Dockerfile updated to use uv
- ✅ pyproject.toml configured correctly
- ✅ .dockerignore updated
- ✅ Documentation updated
- 🚀 Ready to build and deploy!

---

**Updated**: October 22, 2025
**Package Manager**: uv (ultrafast Python package installer)
**Python Version**: 3.11
