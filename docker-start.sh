#!/bin/bash

echo "Starting KIE Document Processing with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if nvidia-docker is available
if command -v nvidia-docker &> /dev/null; then
    echo "Using nvidia-docker for GPU support..."
    DOCKER_COMMAND="nvidia-docker"
elif docker info | grep -q "nvidia"; then
    echo "Using docker with nvidia runtime..."
    DOCKER_COMMAND="docker"
else
    echo "Warning: GPU support not detected. Running in CPU mode."
    DOCKER_COMMAND="docker"
fi

# Create necessary directories
mkdir -p uploads results models

# Build and start the application
echo "Building Docker image..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 10

# Check if the service is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ KIE Document Processing is running at http://localhost:8000"
    echo ""
    echo "🐳 Docker Commands:"
    echo "  View logs: docker-compose logs -f"
    echo "  Stop: docker-compose down"
    echo "  Restart: docker-compose restart"
    echo ""
    echo "📊 GPU Usage:"
    echo "  Monitor: watch -n 1 nvidia-smi"
else
    echo "❌ Service failed to start. Check logs:"
    docker-compose logs
fi