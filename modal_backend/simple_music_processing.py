#!/usr/bin/env python3
"""
Simple music processing endpoint for Modal deployment
This endpoint processes music files and returns note data (without video generation for now)
"""

import modal
from datetime import datetime
from typing import Dict, Any

# Create Modal app
app = modal.App("musicsynth-simple-music")

# Define the Modal image with required dependencies
processing_image = (
    modal.Image.debian_slim()
    .pip_install([
        "numpy>=1.26.0",
        "pillow>=10.2.0", 
        "oemer==0.1.5",
        "onnx>=1.15.0",
        "onnxruntime>=1.17.0",
        "tensorflow>=2.15.0",
        "keras>=2.15.0",
        "fastapi[standard]>=0.104.1",
        "python-multipart>=0.0.6"
    ])
    .apt_install([
        "ffmpeg",
        "libsndfile1"
    ])
)

@app.function(image=processing_image)
@modal.fastapi_endpoint(docs=True)
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "musicsynth-simple-music",
        "message": "MusicSynth Simple Music Processing API is running!"
    }

@app.function(
    image=processing_image,
    gpu="T4",  # Use T4 GPU for faster processing
    timeout=600,  # 10 minutes timeout
    memory=2048,  # 2GB memory
)
@modal.fastapi_endpoint(method="POST", docs=True)
def process_music_file(data: dict) -> Dict[str, Any]:
    """Process music file and extract note data"""
    import os
    import tempfile
    import uuid
    import xml.etree.ElementTree as ET
    import subprocess
    import base64
    
    try:
        # Extract file data from the request
        file_content_b64 = data.get("file_content", "")
        filename = data.get("filename", "unknown.txt")
        
        # Decode base64 file content
        file_content = base64.b64decode(file_content_b64)
        
        # Create temporary directories
        with tempfile.TemporaryDirectory() as temp_dir:
            session_id = str(uuid.uuid4())
            
            # Determine file type
            filename_lower = filename.lower()
            is_musicxml = filename_lower.endswith('.musicxml') or filename_lower.endswith('.xml')
            is_image = filename_lower.endswith('.png') or filename_lower.endswith('.jpg') or filename_lower.endswith('.jpeg')
            
            if not (is_musicxml or is_image):
                return {
                    "success": False,
                    "message": "Please upload a MusicXML file (.musicxml, .xml) or an image file (.png, .jpg, .jpeg)",
                    "notes": None
                }
            
            # Save uploaded file
            input_file_path = os.path.join(temp_dir, filename)
            with open(input_file_path, 'wb') as f:
                f.write(file_content)
            
            # Process image files with Oemer to extract MusicXML
            if is_image:
                print(f"Processing image with Oemer: {input_file_path}")
                cmd = ["oemer", "-o", temp_dir, "--save-cache", "-d", input_file_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    return {
                        "success": False,
                        "message": f"Oemer failed to process image: {result.stderr}",
                        "notes": None
                    }
                
                # Find the output MusicXML file
                basename = os.path.splitext(os.path.basename(input_file_path))[0]
                musicxml_path = os.path.join(temp_dir, f"{basename}.musicxml")
                if not os.path.exists(musicxml_path):
                    musicxml_path = os.path.join(temp_dir, f"{basename}.xml")
                    if not os.path.exists(musicxml_path):
                        return {
                            "success": False,
                            "message": f"Oemer did not produce a MusicXML file for {basename}",
                            "notes": None
                        }
                
                print(f"Oemer produced MusicXML file: {musicxml_path}")
            else:
                # Use the uploaded MusicXML file directly
                musicxml_path = input_file_path
                print(f"Using uploaded MusicXML file: {musicxml_path}")
            
            # Parse the MusicXML file
            print(f"Parsing MusicXML file: {musicxml_path}")
            notes = parse_musicxml(musicxml_path)
            
            if not notes:
                return {
                    "success": False,
                    "message": "No notes found in the MusicXML file",
                    "notes": None
                }
            
            return {
                "success": True,
                "message": f"Music file processed successfully from {filename}",
                "notes": notes,
                "notes_count": len(notes),
                "filename": filename,
                "timestamp": datetime.now().isoformat(),
                "note": "Video generation will be implemented in the next version"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing file: {str(e)}",
            "notes": None,
            "timestamp": datetime.now().isoformat()
        }

def parse_musicxml(file_path):
    """Parse musicxml file and extract notes with timing information."""
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    notes = []
    current_time = 0
    
    # Find divisions (ticks per quarter note)
    divisions_elem = root.find('.//divisions')
    if divisions_elem is None:
        print("Warning: No divisions found in MusicXML, using default value")
        divisions = 1
    else:
        divisions = int(divisions_elem.text)
    
    # Process each measure
    for measure in root.findall('.//measure'):
        for note in measure.findall('note'):
            # Skip rests
            if note.find('rest') is not None:
                if note.find('duration') is not None:
                    duration = int(note.find('duration').text)
                    current_time += duration / divisions
                continue
            
            # Get pitch information
            pitch = note.find('pitch')
            if pitch is None:
                continue
                
            step = pitch.find('step').text
            octave = pitch.find('octave').text
            
            # Check for accidentals
            alter_elem = pitch.find('alter')
            alter = 0
            if alter_elem is not None:
                alter = int(alter_elem.text)
            
            # Determine the note name
            accidental = ""
            if alter == 1:
                accidental = "#"
            elif alter == -1:
                accidental = "b"
            
            note_name = f"{step}{accidental}{octave}"
            
            # Get duration
            duration = int(note.find('duration').text)
            duration_in_seconds = duration / divisions
            
            # Add the note to our list
            notes.append({
                "note": note_name,
                "start_time": current_time,
                "duration": duration_in_seconds
            })
            
            current_time += duration_in_seconds
    
    return notes

if __name__ == "__main__":
    # Deploy the functions to Modal
    app.deploy() 