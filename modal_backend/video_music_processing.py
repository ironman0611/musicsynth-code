#!/usr/bin/env python3
"""
Video music processing endpoint for Modal deployment
This endpoint processes music files and generates actual videos
"""

import modal
from datetime import datetime
from typing import Dict, Any

# Create Modal app
app = modal.App("musicsynth-video-music")

# Define the Modal image with all required dependencies including moviepy
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
        "service": "musicsynth-video-music",
        "message": "MusicSynth Video Music Processing API is running!"
    }

@app.function(
    image=processing_image,
    gpu="T4",  # Use T4 GPU for faster processing
    timeout=600,  # 10 minutes timeout
    memory=2048,  # 2GB memory
)
@modal.fastapi_endpoint(method="POST", docs=True)
def process_music_file(data: dict) -> Dict[str, Any]:
    """Process music file and generate video visualization"""
    import os
    import tempfile
    import uuid
    import xml.etree.ElementTree as ET
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
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
                    "video_data": None
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
                        "video_data": None
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
                            "video_data": None
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
                    "video_data": None
                }
            
            # Generate output video path
            output_filename = os.path.splitext(os.path.basename(musicxml_path))[0] + '_visualization.mp4'
            output_path = os.path.join(temp_dir, output_filename)
            
            # Create the video
            print(f"Generating video: {output_path}")
            make_video(notes, output_file=output_path)
            
            # Read the generated video file
            with open(output_path, 'rb') as video_file:
                video_data = video_file.read()
            
            # Encode video data as base64 for JSON response
            video_data_b64 = base64.b64encode(video_data).decode('utf-8')
            
            return {
                "success": True,
                "message": f"Video generated successfully from {filename}",
                "video_data": video_data_b64,
                "filename": output_filename,
                "notes_count": len(notes),
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing file: {str(e)}",
            "video_data": None,
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

def make_video(notes, output_file="violin_tutorial.mp4", fps=30):
    """Generate a Synthesia-like video for violin from notes data."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    import subprocess
    import os
    
    # Video settings
    width, height = 800, 600
    duration = max(note["start_time"] + note["duration"] for note in notes) + 2  # Add 2 seconds buffer
    
    # Create frames directory
    frames_dir = os.path.join(os.path.dirname(output_file), "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    # Generate frames
    frame_count = int(duration * fps)
    print(f"Generating {frame_count} frames...")
    
    for frame_num in range(frame_count):
        t = frame_num / fps
        
        # Create a frame
        img = Image.new('RGB', (width, height), color='black')
        draw = ImageDraw.Draw(img)
        
        # Draw piano keys (simplified)
        key_width = width // 52  # 52 white keys
        for i in range(52):
            x = i * key_width
            draw.rectangle([x, height//2, x + key_width - 1, height], fill='white', outline='gray')
        
        # Draw notes at their time positions
        for note in notes:
            note_start = note["start_time"]
            note_duration = note["duration"]
            
            if note_start <= t <= note_start + note_duration:
                # Calculate position based on note name
                note_name = note["note"]
                # Simple mapping of note to position (you can make this more sophisticated)
                note_pos = hash(note_name) % 52
                x = note_pos * key_width
                
                # Draw the note
                draw.rectangle([x, height//2 - 50, x + key_width - 1, height//2], 
                             fill='red', outline='white')
                
                # Draw note name
                try:
                    font = ImageFont.load_default()
                    draw.text((x + 5, height//2 - 45), note_name, fill='white', font=font)
                except:
                    pass
        
        # Save frame
        frame_path = os.path.join(frames_dir, f"frame_{frame_num:04d}.png")
        img.save(frame_path)
    
    # Use ffmpeg to create video from frames
    print("Creating video with ffmpeg...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",  # Overwrite output file
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_file
    ]
    
    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"FFmpeg failed: {result.stderr}")
    
    # Clean up frames
    import shutil
    shutil.rmtree(frames_dir)
    
    print(f"Video created: {output_file}")
    return output_file

if __name__ == "__main__":
    # Deploy the functions to Modal
    app.deploy() 