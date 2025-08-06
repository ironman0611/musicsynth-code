#!/bin/bash

# MusicSynth API Startup Script

echo "🎵 Starting MusicSynth API Server..."
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import fastapi, uvicorn, moviepy, PIL, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing. Installing..."
    pip install -r api_requirements.txt
fi

# Check if Oemer is available
if ! command -v oemer &> /dev/null; then
    echo "⚠️  Warning: Oemer is not installed or not in PATH"
    echo "   Image processing will not work without Oemer"
    echo "   Please install Oemer for full functionality"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p temp xml_files

# Start the API server
echo "🚀 Starting API server on http://localhost:8000"
echo "📖 API Documentation will be available at:"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 api_server.py 