#!/usr/bin/env python3
"""
Test script for the MusicSynth Modal API
This script demonstrates how to use the Modal API endpoints for image to video generation.
"""

import requests
import base64
import json
import os
from pathlib import Path

def test_modal_api():
    """Test the Modal API endpoints"""
    
    # You'll need to get the actual Modal endpoint URL after deployment
    # This is a placeholder - replace with your actual Modal endpoint
    MODAL_BASE_URL = "https://your-modal-endpoint.modal.run"
    
    print("🎵 MusicSynth Modal API Test")
    print("=" * 40)
    print(f"Testing against: {MODAL_BASE_URL}")
    print()
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{MODAL_BASE_URL}/health")
        print(f"Health Check Response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy! Service: {data.get('service', 'Unknown')}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Test with an image file if available
    test_image_path = "music2.jpg"
    if os.path.exists(test_image_path):
        print(f"\n2. Testing process-image endpoint with {test_image_path}...")
        test_process_image_modal(MODAL_BASE_URL, test_image_path)
    else:
        print(f"\n2. Skipping image test - {test_image_path} not found")
    
    # Test with a MusicXML file if available
    xml_dir = Path("xml_files")
    if xml_dir.exists():
        xml_files = list(xml_dir.glob("*.musicxml")) + list(xml_dir.glob("*.xml"))
        if xml_files:
            test_xml_path = str(xml_files[0])
            print(f"\n3. Testing process-musicxml endpoint with {test_xml_path}...")
            test_process_musicxml_modal(MODAL_BASE_URL, test_xml_path)
        else:
            print("\n3. Skipping MusicXML test - no MusicXML files found in xml_files directory")
    else:
        print("\n3. Skipping MusicXML test - xml_files directory not found")
    
    print("\nTest completed!")

def test_process_image_modal(modal_url: str, image_path: str):
    """
    Test the Modal process-image endpoint with an uploaded image
    
    Args:
        modal_url: Modal API base URL
        image_path: Path to the image file to upload
    """
    try:
        # Read the image file and encode as base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Prepare the request data
        request_data = {
            "file_content": image_b64,
            "filename": os.path.basename(image_path)
        }
        
        print(f"Uploading image: {image_path}")
        
        # Make the request to Modal
        response = requests.post(f"{modal_url}/process-image", json=request_data)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Video generated:")
            print(f"  - Message: {result['message']}")
            print(f"  - Notes count: {result['notes_count']}")
            print(f"  - Filename: {result['filename']}")
            print(f"  - Session ID: {result['session_id']}")
            
            # Save the video data to a file
            video_data = base64.b64decode(result['video_data'])
            output_filename = f"modal_generated_{result['filename']}"
            with open(output_filename, 'wb') as f:
                f.write(video_data)
            print(f"  - Video saved as: {output_filename}")
            
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Error testing Modal process-image endpoint: {e}")
        return False

def test_process_musicxml_modal(modal_url: str, musicxml_path: str):
    """
    Test the Modal process-musicxml endpoint with an uploaded MusicXML file
    
    Args:
        modal_url: Modal API base URL
        musicxml_path: Path to the MusicXML file to upload
    """
    try:
        # Read the MusicXML file and encode as base64
        with open(musicxml_path, 'rb') as f:
            xml_data = f.read()
            xml_b64 = base64.b64encode(xml_data).decode('utf-8')
        
        # Prepare the request data
        request_data = {
            "file_content": xml_b64,
            "filename": os.path.basename(musicxml_path)
        }
        
        print(f"Uploading MusicXML file: {musicxml_path}")
        
        # Make the request to Modal
        response = requests.post(f"{modal_url}/process-musicxml", json=request_data)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success! Video generated:")
            print(f"  - Message: {result['message']}")
            print(f"  - Notes count: {result['notes_count']}")
            print(f"  - Filename: {result['filename']}")
            print(f"  - Session ID: {result['session_id']}")
            
            # Save the video data to a file
            video_data = base64.b64decode(result['video_data'])
            output_filename = f"modal_generated_{result['filename']}"
            with open(output_filename, 'wb') as f:
                f.write(video_data)
            print(f"  - Video saved as: {output_filename}")
            
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Error testing Modal process-musicxml endpoint: {e}")
        return False

def deploy_to_modal():
    """Deploy the Modal API"""
    print("🚀 Deploying MusicSynth API to Modal...")
    print("This will create the Modal endpoints and return the deployment URL.")
    print()
    
    try:
        # Import modal and deploy
        import modal
        
        # This will deploy the app defined in modal_api_server.py
        print("Running: python modal_api_server.py")
        print("This will deploy the API to Modal and provide you with the endpoint URLs.")
        print()
        print("After deployment, you'll get URLs like:")
        print("- https://your-app--health.modal.run")
        print("- https://your-app--process-image.modal.run")
        print("- https://your-app--process-musicxml.modal.run")
        print()
        print("Update the MODAL_BASE_URL in this script with the actual endpoint URL.")
        
    except ImportError:
        print("❌ Modal is not installed. Install it with:")
        print("pip install modal")
        return False
    
    return True

if __name__ == "__main__":
    print("MusicSynth Modal API Test Script")
    print("=" * 50)
    print()
    
    # Check if we should deploy or test
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        deploy_to_modal()
    else:
        print("To deploy to Modal, run: python test_modal_api.py deploy")
        print("To test the API, update MODAL_BASE_URL and run: python test_modal_api.py")
        print()
        test_modal_api() 