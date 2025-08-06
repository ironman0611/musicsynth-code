#!/usr/bin/env python3
"""
Test script for the simple music processing endpoint
"""

import requests
import json
import base64

# The deployed endpoint URLs
BASE_URLS = {
    "health": "https://cotoyota09--musicsynth-simple-music-health.modal.run",
    "process_music": "https://cotoyota09--musicsynth-simple-music-process-music-file.modal.run"
}

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get(BASE_URLS["health"])
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful: {data}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_music_processing_endpoint():
    """Test the music processing endpoint with a sample MusicXML file"""
    print("🎵 Testing music processing endpoint...")
    
    # Sample MusicXML content
    sample_musicxml = """<?xml version="1.0" encoding="UTF-8"?>
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
    
    try:
        # Encode the MusicXML content as base64
        file_content_b64 = base64.b64encode(sample_musicxml.encode('utf-8')).decode('utf-8')
        
        # Prepare the request data
        test_data = {
            "file_content": file_content_b64,
            "filename": "test_song.musicxml"
        }
        
        print("📤 Sending MusicXML file for processing...")
        response = requests.post(
            BASE_URLS["process_music"],
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Music processing successful!")
            print(f"📝 Notes processed: {data.get('notes_count', 0)}")
            print(f"💬 Message: {data.get('message', '')}")
            
            # Display the extracted notes
            if data.get('notes'):
                print(f"🎵 Extracted notes:")
                for i, note in enumerate(data['notes'][:5]):  # Show first 5 notes
                    print(f"   {i+1}. {note['note']} (start: {note['start_time']:.2f}s, duration: {note['duration']:.2f}s)")
                if len(data['notes']) > 5:
                    print(f"   ... and {len(data['notes']) - 5} more notes")
            
            return True
        else:
            print(f"❌ Music processing failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Music processing failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Simple Music Processing Endpoints")
    print("=" * 50)
    print("🌐 Endpoint URLs:")
    for name, url in BASE_URLS.items():
        print(f"• {name}: {url}")
    print()
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    print()
    
    # Test music processing endpoint
    music_ok = test_music_processing_endpoint()
    print()
    
    # Summary
    print("📊 Test Results:")
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Music Processing Endpoint: {'✅ PASS' if music_ok else '❌ FAIL'}")
    
    if health_ok and music_ok:
        print("\n🎉 All tests passed! Your music processing endpoints are working correctly!")
        print("\n📋 Available endpoints:")
        print(f"• GET  {BASE_URLS['health']}")
        print(f"• POST {BASE_URLS['process_music']} (with JSON body)")
        print("\n💡 The music processing endpoint can:")
        print("   - Process MusicXML files (.musicxml, .xml)")
        print("   - Process image files (.png, .jpg, .jpeg) using Oemer OCR")
        print("   - Extract note data with timing information")
        print("   - Return structured JSON with note details")
        print("\n🚀 Next steps:")
        print("   - Integrate with frontend for file upload")
        print("   - Add video generation capability")
        print("   - Implement real-time processing status")
    else:
        print("\n⚠️  Some tests failed. Please check the deployment.")

if __name__ == "__main__":
    main() 