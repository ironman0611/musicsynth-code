#!/usr/bin/env python3
"""
Test script for video generation endpoint
"""

import requests
import base64
import json
import time

# Sample MusicXML content for testing
SAMPLE_MUSICXML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="3.1">
  <part-list>
    <score-part id="P1">
      <part-name>Music</part-name>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>1</divisions>
        <key>
          <fifths>0</fifths>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>C</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>D</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>E</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>F</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
    </measure>
    <measure number="2">
      <note>
        <pitch>
          <step>G</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>A</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>B</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
    </measure>
  </part>
</score-partwise>"""

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    
    url = "https://cotoyota09--musicsynth-video-music-health.modal.run"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            print("✅ Health check successful!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_video_generation():
    """Test the video generation endpoint"""
    print("\n🎵 Testing video generation...")
    
    url = "https://cotoyota09--musicsynth-video-music-process-music-file.modal.run"
    
    # Prepare the request data
    file_content_b64 = base64.b64encode(SAMPLE_MUSICXML.encode('utf-8')).decode('utf-8')
    
    data = {
        "file_content": file_content_b64,
        "filename": "test_scale.musicxml"
    }
    
    try:
        print("📤 Sending request to video generation endpoint...")
        print(f"URL: {url}")
        print(f"File size: {len(SAMPLE_MUSICXML)} bytes")
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=300)  # 5 minute timeout
        end_time = time.time()
        
        print(f"⏱️  Request took {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Video generation successful!")
            print(f"Message: {result.get('message', 'No message')}")
            print(f"Notes count: {result.get('notes_count', 'Unknown')}")
            print(f"Filename: {result.get('filename', 'Unknown')}")
            
            # Check if video data was returned
            video_data = result.get('video_data')
            if video_data:
                video_bytes = base64.b64decode(video_data)
                print(f"📹 Video generated! Size: {len(video_bytes)} bytes")
                
                # Save the video locally
                output_filename = result.get('filename', 'generated_video.mp4')
                with open(output_filename, 'wb') as f:
                    f.write(video_bytes)
                print(f"💾 Video saved as: {output_filename}")
                
                return True
            else:
                print("❌ No video data returned")
                return False
        else:
            print(f"❌ Video generation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Video generation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing MusicSynth Video Generation")
    print("=" * 50)
    
    # Test health first
    health_ok = test_health()
    
    if not health_ok:
        print("\n❌ Health check failed. Skipping video generation test.")
        return
    
    # Test video generation
    video_ok = test_video_generation()
    
    # Summary
    print("\n📊 Test Results:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Video Generation: {'✅ PASS' if video_ok else '❌ FAIL'}")
    
    if health_ok and video_ok:
        print("\n🎉 All tests passed! Video generation is working!")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main() 