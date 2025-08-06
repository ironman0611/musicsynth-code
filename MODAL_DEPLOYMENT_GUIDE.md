# MusicSynth Modal Deployment Guide

This guide will help you deploy the MusicSynth API endpoints to Modal for cloud-based image to video generation.

## Prerequisites

1. **Modal Account**: Sign up at [modal.com](https://modal.com)
2. **Modal CLI**: Install the Modal CLI
   ```bash
   pip install modal
   ```
3. **Authentication**: Authenticate with Modal
   ```bash
   modal token new
   ```

## Deployment Steps

### 1. Deploy the API to Modal

Run the deployment command:

```bash
python modal_api_server.py
```

This will:
- Create a Modal app named "musicsynth-api"
- Deploy three endpoints:
  - `/health` - Health check endpoint
  - `/process-image` - Image processing endpoint
  - `/process-musicxml` - MusicXML processing endpoint

### 2. Get Your Endpoint URLs

After deployment, Modal will provide you with endpoint URLs like:
```
https://your-app--health.modal.run
https://your-app--process-image.modal.run
https://your-app--process-musicxml.modal.run
```

### 3. Test the Deployment

Update the `MODAL_BASE_URL` in `test_modal_api.py` with your actual endpoint URL and run:

```bash
python test_modal_api.py
```

## API Endpoints

### Health Check
- **URL**: `GET /health`
- **Description**: Check if the API is running
- **Response**: JSON with status and timestamp

### Process Image
- **URL**: `POST /process-image`
- **Description**: Upload a sheet music image and generate a video visualization
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "file_content": "base64_encoded_image_data",
    "filename": "image.jpg"
  }
  ```
- **Response**: JSON with video data and metadata

### Process MusicXML
- **URL**: `POST /process-musicxml`
- **Description**: Upload a MusicXML file and generate a video visualization
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "file_content": "base64_encoded_xml_data",
    "filename": "sheet_music.xml"
  }
  ```
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

## Example Usage

### Using Python

```python
import requests
import base64

# Process an image
with open('music2.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

request_data = {
    "file_content": image_data,
    "filename": "music2.jpg"
}

response = requests.post(
    "https://your-app--process-image.modal.run",
    json=request_data
)

if response.status_code == 200:
    result = response.json()
    
    # Save the video
    video_data = base64.b64decode(result['video_data'])
    with open('output_video.mp4', 'wb') as f:
        f.write(video_data)
    
    print(f"Video generated with {result['notes_count']} notes")
```

### Using curl

```bash
# Encode image as base64
IMAGE_B64=$(base64 -w 0 music2.jpg)

# Send request
curl -X POST "https://your-app--process-image.modal.run" \
  -H "Content-Type: application/json" \
  -d "{\"file_content\":\"$IMAGE_B64\",\"filename\":\"music2.jpg\"}"
```

## Modal Configuration

The Modal deployment includes:

- **GPU Support**: T4 GPU for faster video processing
- **Memory**: 2GB RAM for processing large files
- **Timeout**: 10 minutes for video generation
- **Dependencies**: All required packages including Oemer, MoviePy, TensorFlow, etc.

## Monitoring and Logs

You can monitor your Modal deployment:

1. **Modal Dashboard**: Visit [modal.com](https://modal.com) to view your deployments
2. **Logs**: Check logs in the Modal dashboard for debugging
3. **Metrics**: Monitor performance and usage in the dashboard

## Troubleshooting

### Common Issues

1. **Deployment Fails**
   - Check Modal authentication: `modal token new`
   - Verify internet connection
   - Check Modal account status

2. **Processing Fails**
   - Ensure image contains readable sheet music
   - Check file format (PNG, JPG, JPEG for images)
   - Verify MusicXML format for XML files

3. **Timeout Errors**
   - Large files may take longer to process
   - Consider optimizing image quality
   - Check Modal resource limits

### Debugging

1. **Check Modal Logs**:
   ```bash
   modal app logs musicsynth-api
   ```

2. **Test Individual Endpoints**:
   ```bash
   curl https://your-app--health.modal.run
   ```

3. **Verify Dependencies**:
   The Modal image includes all required dependencies:
   - Oemer for image processing
   - MoviePy for video generation
   - TensorFlow for ML components
   - FFmpeg for video encoding

## Cost Optimization

Modal charges based on:
- **Compute time**: GPU usage during processing
- **Memory usage**: RAM consumption
- **Network**: Data transfer

Tips to optimize costs:
- Use appropriate image sizes (not too large)
- Process files during off-peak hours
- Monitor usage in Modal dashboard

## Security Considerations

- **Authentication**: Consider adding API keys for production
- **Rate Limiting**: Implement rate limiting for public endpoints
- **File Validation**: Validate file types and sizes
- **CORS**: Configure CORS properly for web applications

## Production Deployment

For production use:

1. **Environment Variables**: Set production environment variables
2. **Monitoring**: Set up proper monitoring and alerting
3. **Backup**: Implement backup strategies for important data
4. **Scaling**: Configure auto-scaling based on demand

## Support

- **Modal Documentation**: [docs.modal.com](https://docs.modal.com)
- **Modal Community**: [community.modal.com](https://community.modal.com)
- **GitHub Issues**: Report issues in the project repository

## Next Steps

After successful deployment:

1. **Integrate with Frontend**: Use the endpoints in your web application
2. **Add Authentication**: Implement API key authentication
3. **Monitor Usage**: Set up monitoring and analytics
4. **Scale**: Configure auto-scaling based on demand
5. **Optimize**: Fine-tune performance and cost

## Example Integration

Here's how to integrate the Modal API with a web frontend:

```javascript
// Frontend JavaScript example
async function processImage(file) {
    const reader = new FileReader();
    reader.onload = async function(e) {
        const base64Data = e.target.result.split(',')[1]; // Remove data URL prefix
        
        const response = await fetch('https://your-app--process-image.modal.run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file_content: base64Data,
                filename: file.name
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            // Handle the video data
            const videoBlob = new Blob(
                [Uint8Array.from(atob(result.video_data), c => c.charCodeAt(0))],
                { type: 'video/mp4' }
            );
            const videoUrl = URL.createObjectURL(videoBlob);
            // Display the video
            document.getElementById('video').src = videoUrl;
        }
    };
    reader.readAsDataURL(file);
}
```

This deployment guide provides everything you need to successfully deploy and use the MusicSynth API on Modal! 