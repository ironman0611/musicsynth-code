#!/usr/bin/env python3
"""
Test script for health check function
"""

import modal
from datetime import datetime
from typing import Dict, Any

# Create Modal app
app = modal.App("musicsynth-backend")

# Define the Modal image with required dependencies for processing
processing_image = (
    modal.Image.debian_slim()
    .pip_install([
        "numpy>=1.26.0",
        "pillow>=10.2.0", 
        "moviepy>=1.0.3",
        "oemer==0.1.5",
        "onnx>=1.15.0",
        "onnxruntime>=1.17.0",
        "tensorflow>=2.15.0",
        "keras>=2.15.0"
    ])
    .apt_install([
        "ffmpeg",
        "libsndfile1"
    ])
)

# Health check function - doesn't need FastAPI
@app.function(image=processing_image)
def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "musicsynth-backend"
    }

if __name__ == "__main__":
    # Test the health check function
    result = health_check.remote()
    print(f"✅ Health check result: {result}") 