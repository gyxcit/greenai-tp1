@echo off
echo 🐳 Building Green AI Data Story Docker Image...
echo.

REM Build the Docker image
docker build -t green-ai-app .

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Build successful!
    echo.
    echo 🚀 To run the application:
    echo    docker run -p 8501:8501 green-ai-app
    echo.
    echo 🌐 Or with Docker Compose:
    echo    docker-compose up
    echo.
    echo 📱 Access the app at: http://localhost:8501
) else (
    echo.
    echo ❌ Build failed! Please check the error messages above.
    exit /b 1
)

pause