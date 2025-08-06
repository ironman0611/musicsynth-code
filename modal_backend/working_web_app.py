#!/usr/bin/env python3
"""
Working web app for Modal deployment
"""

import modal
from datetime import datetime
from typing import Dict, Any

# Create Modal app
app = modal.App("musicsynth-working")

# Define the Modal image for web endpoints
web_image = (
    modal.Image.debian_slim()
    .pip_install([
        "fastapi[standard]>=0.104.1",
        "python-multipart>=0.0.6",
        "uvicorn>=0.24.0"
    ])
)

@app.function(image=web_image)
def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "musicsynth-working",
        "message": "MusicSynth API is running!"
    }

@app.function(image=web_image)
def process_file(file_content: bytes, filename: str) -> Dict[str, Any]:
    """Process file endpoint"""
    return {
        "success": True,
        "message": f"File {filename} received successfully!",
        "size": len(file_content),
        "timestamp": datetime.now().isoformat()
    }

# Create a working web endpoint
@app.function(image=web_image)
def web_app():
    """Working web app"""
    from fastapi import FastAPI, File, UploadFile, HTTPException
    
    # Create FastAPI app
    app = FastAPI(title="MusicSynth Working API", version="1.0.0")

    @app.get("/")
    async def root():
        """Root endpoint"""
        return {"message": "MusicSynth API is running!"}

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return health_check.remote()

    @app.post("/process")
    async def process(file: UploadFile = File(...)):
        """Process file endpoint"""
        try:
            # Read file content
            file_content = await file.read()
            
            # Process the file
            result = process_file.remote(file_content, file.filename)
            
            return result
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app

if __name__ == "__main__":
    # Deploy the functions to Modal
    app.deploy() 