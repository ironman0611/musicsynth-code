#!/usr/bin/env python3
"""
Test script for the deployed REST endpoints
"""

import requests
import json

# The deployed endpoint URL
BASE_URL = "https://cotoyota09--musicsynth-api-dev.modal.run"

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
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

def test_process_endpoint():
    """Test the process endpoint with a dummy file"""
    print("🎵 Testing process endpoint...")
    
    try:
        # Create a dummy MusicXML content
        test_musicxml = """<?xml version="1.0" encoding="UTF-8"?>
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
          <step>E</step>
          <octave>4</octave>
        </pitch>
        <duration>1</duration>
        <type>quarter</type>
      </note>
    </measure>
  </part>
</score-partwise>"""
        
        # Create a file-like object
        files = {
            'file': ('test.musicxml', test_musicxml.encode('utf-8'), 'application/xml')
        }
        
        response = requests.post(f"{BASE_URL}/process", files=files)
        
        if response.status_code == 200:
            print(f"✅ Process endpoint successful!")
            print(f"📊 Response headers: {dict(response.headers)}")
            print(f"📄 Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"📏 Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
            return True
        else:
            print(f"❌ Process endpoint failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Process endpoint failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Deployed MusicSynth REST Endpoints")
    print("=" * 50)
    print(f"🌐 Base URL: {BASE_URL}")
    print()
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    print()
    
    # Test process endpoint
    process_ok = test_process_endpoint()
    print()
    
    # Summary
    print("📊 Test Results:")
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Process Endpoint: {'✅ PASS' if process_ok else '❌ FAIL'}")
    
    if health_ok and process_ok:
        print("\n🎉 All tests passed! Your REST endpoints are working correctly.")
        print("\n📋 Available endpoints:")
        print(f"• GET  {BASE_URL}/health")
        print(f"• POST {BASE_URL}/process")
    else:
        print("\n⚠️  Some tests failed. Please check the deployment.")

if __name__ == "__main__":
    main() 