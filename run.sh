#!/bin/bash

echo "Starting KIE Document Processing Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads results templates

# Check if GPU is available
if python -c "import torch; print(torch.cuda.is_available())" | grep -q "True"; then
    echo "GPU detected. Using CUDA for inference."
else
    echo "No GPU detected. Using CPU for inference (slower)."
fi

# Start the application
echo "Starting the application on http://localhost:8000"
python app.py