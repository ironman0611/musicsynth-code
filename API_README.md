# MusicSynth API Documentation

This API provides endpoints for processing sheet music images and generating video visualizations.

## Features

- **Image Processing**: Upload sheet music images (PNG, JPG, JPEG) and convert them to video visualizations
- **MusicXML Processing**: Upload MusicXML files directly and generate video visualizations
- **Video Generation**: Create Synthesia-like violin fingerboard visualizations
- **Base64 Response**: Videos are returned as base64-encoded data for easy integration

## Installation

1. Install the required dependencies:
```bash
pip install -r api_requirements.txt
```

2. Ensure Oemer is installed for image processing:
```bash
# Oemer should be installed and available in your PATH
# The API will use the existing Oemer installation
```

## Running the API Server

Start the API server:
```bash
python api_server.py
```

The server will run on `http://localhost:8000` by default.

## API Endpoints

### 1. Health Check
- **URL**: `GET /health`
- **Description**: Check if the API is running
- **Response**: JSON with status and timestamp

### 2. Process Image
- **URL**: `POST /process-image`
- **Description**: Upload a sheet music image and generate a video visualization
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: Image file (PNG, JPG, JPEG)
- **Response**: JSON with video data and metadata

### 3. Process MusicXML
- **URL**: `POST /process-musicxml`
- **Description**: Upload a MusicXML file and generate a video visualization
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: MusicXML file (.musicxml, .xml)
- **Response**: JSON with video data and metadata

## Response Format

All endpoints return JSON responses with the following structure:

```json
{
  "success": true,
  "message": "Video generated successfully from filename.jpg",
  "video_data": "base64_encoded_video_data",
  "filename": "output_filename.mp4",
  "notes_count": 42,
  "timestamp": "2024-01-01T12:00:00.000000",
  "session_id": "uuid-string"
}
```

## Error Responses

Errors are returned with appropriate HTTP status codes:

```json
{
  "detail": "Error message describing the issue"
}
```

## Example Usage

### Using curl

1. **Process an image**:
```bash
curl -X POST "http://localhost:8000/process-image" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@music2.jpg"
```

2. **Process a MusicXML file**:
```bash
curl -X POST "http://localhost:8000/process-musicxml" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sheet_music.xml"
```

### Using Python

```python
import requests
import base64

# Process an image
with open('music2.jpg', 'rb') as f:
    files = {'file': ('music2.jpg', f, 'image/jpeg')}
    response = requests.post('http://localhost:8000/process-image', files=files)

if response.status_code == 200:
    result = response.json()
    
    # Save the video
    video_data = base64.b64decode(result['video_data'])
    with open('output_video.mp4', 'wb') as f:
        f.write(video_data)
    
    print(f"Video generated with {result['notes_count']} notes")
```

## Testing

Run the test script to verify the API is working:

```bash
python test_api.py
```

This will:
1. Test the health endpoint
2. Test image processing with `music2.jpg` (if available)
3. Test MusicXML processing with files from the `xml_files` directory (if available)

## API Documentation

When the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

The API uses the following key dependencies:
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **Oemer**: Optical Music Recognition for processing images
- **MoviePy**: Video generation
- **Pillow**: Image processing
- **NumPy**: Numerical computations

## Architecture

The API follows this workflow:

1. **Image Upload**: Client uploads an image file
2. **OCR Processing**: Oemer processes the image to extract MusicXML
3. **MusicXML Parsing**: The extracted MusicXML is parsed to extract notes
4. **Video Generation**: A Synthesia-like video is generated using MoviePy
5. **Response**: Video is encoded as base64 and returned to client

## Error Handling

The API includes comprehensive error handling for:
- Invalid file types
- Oemer processing failures
- MusicXML parsing errors
- Video generation failures
- File system errors

## Security Notes

- CORS is enabled for all origins (configure properly for production)
- File uploads are validated for type and content
- Temporary files are cleaned up automatically
- No persistent storage of uploaded files

## Performance Considerations

- Videos are generated in memory and returned as base64
- Large files may take time to process
- Consider implementing async processing for production use
- Temporary directories are used for processing to avoid disk space issues 