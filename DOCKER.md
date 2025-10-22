# Docker Deployment Guide

This guide explains how to build and run the Power & Gas Trader Shift Handover application using Docker.

## Prerequisites

- Docker Desktop installed on your system
- Docker Compose (included with Docker Desktop)

## Technology Stack

- **Python**: 3.11
- **Package Manager**: uv (ultrafast Python package installer)
- **Dependencies**: Managed via `pyproject.toml`
- **Database**: SQLite3
- **Web Framework**: Streamlit

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start the application:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   Open your browser and navigate to `http://localhost:8501`

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

4. **View logs:**
   ```bash
   docker-compose logs -f
   ```

### Using Docker CLI

1. **Build the Docker image:**
   ```bash
   docker build -t shift-handover:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8501:8501 -v shift-handover-data:/app/data --name shift-handover shift-handover:latest
   ```

3. **Stop the container:**
   ```bash
   docker stop shift-handover
   docker rm shift-handover
   ```

## Development Mode

For development with hot-reload enabled, use the development Docker Compose file:

```bash
docker-compose -f docker-compose.dev.yml up
```

This mounts your source code as volumes, allowing you to make changes without rebuilding the image.

## Database Persistence

The SQLite database is stored in a Docker volume named `shift-handover-data`. This ensures your data persists even when containers are stopped or removed.

### Backup Database

```bash
# Copy database from volume to local directory
docker run --rm -v shift-handover-data:/data -v ${PWD}:/backup alpine cp /data/shift_handover.db /backup/
```

### Restore Database

```bash
# Copy database from local directory to volume
docker run --rm -v shift-handover-data:/data -v ${PWD}:/backup alpine cp /backup/shift_handover.db /data/
```

## Environment Variables

You can customize the application using environment variables:

- `DB_PATH`: Path to SQLite database (default: `/app/data/shift_handover.db`)

Example:
```yaml
environment:
  - DB_PATH=/app/data/custom_db.db
```

## Health Checks

The container includes a health check that monitors the Streamlit application. You can view the health status:

```bash
docker ps
```

Look for the `STATUS` column showing `healthy` or `unhealthy`.

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Or for specific container
docker logs shift-handover-app
```

### Permission issues
If you encounter permission issues with volumes, ensure Docker has the necessary permissions to access the mount points.

### Port already in use
If port 8501 is already in use, modify the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8080:8501"  # Use port 8080 instead
```

## Production Deployment

For production deployment:

1. **Build optimized image:**
   ```bash
   docker build -t shift-handover:production .
   ```

2. **Use production compose file:**
   - Remove volume mounts for source code
   - Set appropriate restart policies
   - Configure proper logging

3. **Resource limits:**
   Add resource constraints to `docker-compose.yml`:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1'
         memory: 512M
       reservations:
         cpus: '0.5'
         memory: 256M
   ```

## Multi-stage Build (Optional)

For a smaller production image, consider using multi-stage builds. Update the Dockerfile:

```dockerfile
# Builder stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["streamlit", "run", "app.py", ...]
```

## Security Best Practices

1. **Don't run as root:** Consider adding a non-root user in the Dockerfile
2. **Scan for vulnerabilities:** Use `docker scan shift-handover:latest`
3. **Keep base image updated:** Regularly rebuild with latest Python image
4. **Use secrets:** For sensitive data, use Docker secrets instead of environment variables

## Support

For issues or questions, refer to the main README.md or project documentation.
