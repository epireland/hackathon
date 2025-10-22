@echo off
REM Build and run the Docker container for Shift Handover application

echo Building Shift Handover Docker image...
docker build -t shift-handover:latest .

if %ERRORLEVEL% NEQ 0 (
    echo Build failed!
    exit /b %ERRORLEVEL%
)

echo.
echo Build successful!
echo.
echo Starting container with Docker Compose...
docker-compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo Failed to start container!
    exit /b %ERRORLEVEL%
)

echo.
echo Container started successfully!
echo.
echo Access the application at: http://localhost:8501
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
