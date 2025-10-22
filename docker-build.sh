#!/bin/bash
# Build and run the Docker container for Shift Handover application

echo "Building Shift Handover Docker image..."
docker build -t shift-handover:latest .

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

echo ""
echo "Build successful!"
echo ""
echo "Starting container with Docker Compose..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "Failed to start container!"
    exit 1
fi

echo ""
echo "Container started successfully!"
echo ""
echo "Access the application at: http://localhost:8501"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
