#!/bin/bash

echo "🐳 Building Green AI Data Story Docker Image..."
echo

# Build the Docker image
docker build -t green-ai-app .

if [ $? -eq 0 ]; then
    echo
    echo "✅ Build successful!"
    echo
    echo "🚀 To run the application:"
    echo "   docker run -p 8501:8501 green-ai-app"
    echo
    echo "🌐 Or with Docker Compose:"
    echo "   docker-compose up"
    echo
    echo "📱 Access the app at: http://localhost:8501"
else
    echo
    echo "❌ Build failed! Please check the error messages above."
    exit 1
fi