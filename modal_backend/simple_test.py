#!/usr/bin/env python3
"""
Simple test for Modal functions
"""

import modal
from datetime import datetime
from typing import Dict, Any

# Create Modal app
app = modal.App("musicsynth-simple-test")

# Define the Modal image
image = (
    modal.Image.debian_slim()
    .pip_install([
        "fastapi[standard]>=0.104.1",
        "python-multipart>=0.0.6",
        "uvicorn>=0.24.0"
    ])
)

@app.function(image=image)
def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "musicsynth-simple-test",
        "message": "MusicSynth API is running!"
    }

@app.function(image=image)
def process_file(file_content: str, filename: str) -> Dict[str, Any]:
    """Process file endpoint"""
    return {
        "success": True,
        "message": f"File {filename} received successfully!",
        "size": len(file_content),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Test the functions
    print("🧪 Testing Modal Functions")
    print("=" * 30)
    
    # Test health check
    print("🔍 Testing health check...")
    try:
        result = health_check.remote()
        print(f"✅ Health check successful: {result}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test process file
    print("\n🎵 Testing process file...")
    try:
        test_content = "test file content"
        result = process_file.remote(test_content, "test.txt")
        print(f"✅ Process file successful: {result}")
    except Exception as e:
        print(f"❌ Process file failed: {e}")
    
    print("\n🎉 Function testing completed!") 