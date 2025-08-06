import streamlit as st
from file_processor import FileProcessor
import os
import time
from datetime import datetime
import pandas as pd
from auth import require_auth, render_user_menu
from config import validate_config
from theme_manager import apply_modern_theme, theme_manager

# Validate configuration first
try:
    validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.info("Please create a .env file in your project root with the required environment variables. Check config.py for details.")
    st.stop()

# Set page config
st.set_page_config(
    page_title="MusicSynth - Transform Sheet Music into Visual Magic",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply MusicSynth theme
apply_modern_theme()

# Check authentication first
if not require_auth():
    st.stop()

# Render user menu in sidebar
render_user_menu()

# Initialize session state for file processor if it doesn't exist
if 'file_processor' not in st.session_state:
    st.session_state.file_processor = FileProcessor()

# Centered container for main content
st.markdown('<div class="centered-container">', unsafe_allow_html=True)

# MusicSynth header with modern branding
st.markdown("""
<div class="modern-header fade-in">
    <h1>🎵 MusicSynth</h1>
    <p>Transform Sheet Music into Visual Magic</p>
    <p class="modern-tagline">Experience the future of music learning</p>
</div>
""", unsafe_allow_html=True)

# Features showcase with modern styling
st.markdown("""
<div class="feature-grid">
    <div class="feature-card fade-in">
        <div class="feature-icon">🎼</div>
        <div class="feature-title">Optical Music Recognition</div>
        <div class="feature-description">Upload sheet music images and watch them transform into digital scores</div>
    </div>
    <div class="feature-card fade-in">
        <div class="feature-icon">🎹</div>
        <div class="feature-title">Visual Piano Roll</div>
        <div class="feature-description">See your music come alive with stunning piano roll animations</div>
    </div>
    <div class="feature-card fade-in">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Music Visualization</div>
        <div class="feature-description">Create beautiful visual representations of your musical compositions</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Environment info with modern styling
is_cloud = os.environ.get('STREAMLIT_SERVER_ENVIRONMENT') == 'cloud'
if is_cloud:
    st.markdown("""
    <div class="status-card warning">
        <div style="font-size: 1.5rem;">☁️</div>
        <div>
            <h3 style="margin: 0 0 0.5rem 0; color: var(--warning); font-weight: 600;">Cloud Environment</h3>
            <p style="margin: 0; color: var(--muted-foreground);">
                Running in cloud mode. Image processing is not available. Please upload MusicXML files for the best experience.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# How to Use section
st.markdown("""
<div class="modern-card">
    <h3>📖 How to Use MusicSynth</h3>
    <p>Follow these simple steps to transform your sheet music into beautiful visual animations</p>
</div>
""", unsafe_allow_html=True)

# Step-by-step guide
st.markdown("""
<div class="modern-card">
    <h4 style="margin: 0 0 1rem 0; color: var(--foreground);">🎯 Step-by-Step Guide:</h4>
    <ol style="margin: 0; padding-left: 1.5rem; color: var(--muted-foreground); line-height: 1.8;">
        <li><strong>Upload Your File:</strong> Choose a MusicXML file or sheet music image</li>
        <li><strong>Wait for Processing:</strong> Our AI will analyze and convert your music</li>
        <li><strong>Preview Animation:</strong> Watch your music come to life</li>
        <li><strong>Download Result:</strong> Save your creation to share with others</li>
        <li><strong>Clean Up:</strong> Remove temporary files when you're done</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Supported formats
st.markdown("""
<div class="modern-card">
    <h4 style="margin: 0 0 1rem 0; color: var(--foreground);">📄 Supported Formats:</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div style="background: var(--muted); padding: 1rem; border-radius: 0.5rem;">
            <h5 style="margin: 0 0 0.5rem 0; color: var(--foreground);">🎼 Music Files:</h5>
            <div style="font-size: 0.875rem; color: var(--muted-foreground);">
                <span style="background: var(--card); padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin: 0.25rem; font-family: monospace; border: 1px solid var(--border);">.musicxml</span>
                <span style="background: var(--card); padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin: 0.25rem; font-family: monospace; border: 1px solid var(--border);">.xml</span>
            </div>
        </div>
        <div style="background: var(--muted); padding: 1rem; border-radius: 0.5rem;">
            <h5 style="margin: 0 0 0.5rem 0; color: var(--foreground);">📷 Sheet Music Images:</h5>
            <div style="font-size: 0.875rem; color: var(--muted-foreground);">
                <span style="background: var(--card); padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin: 0.25rem; font-family: monospace; border: 1px solid var(--border);">.png</span>
                <span style="background: var(--card); padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin: 0.25rem; font-family: monospace; border: 1px solid var(--border);">.jpg</span>
                <span style="background: var(--card); padding: 0.25rem 0.5rem; border-radius: 0.25rem; margin: 0.25rem; font-family: monospace; border: 1px solid var(--border);">.jpeg</span>
            </div>
            <small style="color: var(--muted-foreground); opacity: 0.7;">(desktop only)</small>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# File upload section with modern styling
st.markdown("""
<div class="modern-card">
    <h3>📁 Upload Your Music</h3>
    <p>
        Choose a MusicXML file or upload a sheet music image to begin the transformation
    </p>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Choose your file",
    type=['musicxml', 'xml', 'png', 'jpg', 'jpeg'] if not is_cloud else ['musicxml', 'xml'],
    help="Upload MusicXML files (.musicxml, .xml) or sheet music images (.png, .jpg, .jpeg)"
)

if uploaded_file is not None:
    # Initialize timing statistics
    timing_stats = {
        'start_time': time.time(),
        'steps': {}
    }
    
    # Modern processing section
    st.markdown("""
    <div class="modern-card">
        <h3>⚙️ Creating Magic</h3>
        <p>Converting your music into a stunning visual experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Process the uploaded file
    with st.spinner("🎼 Creating your musical visualization..."):
        # Track file processing time
        process_start = time.time()
        success, message, output_path = st.session_state.file_processor.process_uploaded_file(uploaded_file)
        timing_stats['steps']['file_processing'] = time.time() - process_start
        
        if success:
            st.success(f"✨ {message}")
            
            # Track video generation time
            video_start = time.time()
            
            # Modern video display section
            st.markdown("""
            <div class="modern-card">
                <h3>🎥 Your Musical Magic</h3>
                <p>Your sheet music has been transformed into a beautiful visual piano roll animation</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Try to display the video
            try:
                with open(output_path, 'rb') as video_file:
                    video_bytes = video_file.read()
                    st.video(video_bytes)
            except Exception as e:
                st.warning("Video preview is not available. You can download the video file instead.")
            
            # MusicSynth download section
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with open(output_path, 'rb') as video_file:
                    video_bytes = video_file.read()
                    st.download_button(
                        label="⬇️ Download Your Creation",
                        data=video_bytes,
                        file_name=os.path.basename(output_path),
                        mime="video/mp4",
                        use_container_width=True,
                        type="primary"
                    )
            
            timing_stats['steps']['video_generation'] = time.time() - video_start
            
            # Calculate total time
            timing_stats['total_time'] = time.time() - timing_stats['start_time']
            
            # Modern statistics section
            st.markdown("""
            <div class="modern-card">
                <h3>📊 Processing Performance</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create modern stats display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="modern-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--primary);">{:.2f}s</div>
                        <div style="color: var(--muted-foreground); font-size: 0.875rem; margin-top: 0.5rem;">Music Processing</div>
                    </div>
                </div>
                """.format(timing_stats['steps']['file_processing']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="modern-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--accent);">{:.2f}s</div>
                        <div style="color: var(--muted-foreground); font-size: 0.875rem; margin-top: 0.5rem;">Visual Generation</div>
                    </div>
                </div>
                """.format(timing_stats['steps']['video_generation']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="modern-card">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: var(--success);">{:.2f}s</div>
                        <div style="color: var(--muted-foreground); font-size: 0.875rem; margin-top: 0.5rem;">Total Magic Time</div>
                    </div>
                </div>
                """.format(timing_stats['total_time']), unsafe_allow_html=True)
            
            # Detailed statistics table
            with st.expander("📈 Detailed Performance Metrics"):
                stats_df = pd.DataFrame({
                    'Step': list(timing_stats['steps'].keys()),
                    'Time (seconds)': [f"{t:.2f}" for t in timing_stats['steps'].values()]
                })
                stats_df.loc[len(stats_df)] = ['Total Time', f"{timing_stats['total_time']:.2f}"]
                st.table(stats_df)
            
            # Save timing statistics to a log file
            log_entry = f"\n{datetime.now()}\n"
            log_entry += f"File: {uploaded_file.name}\n"
            for step, duration in timing_stats['steps'].items():
                log_entry += f"{step}: {duration:.2f} seconds\n"
            log_entry += f"Total Time: {timing_stats['total_time']:.2f} seconds\n"
            log_entry += "-" * 50
            
            log_path = os.path.join(st.session_state.file_processor.temp_dir, 'processing_stats.log')
            with open(log_path, 'a') as f:
                f.write(log_entry)
        else:
            st.error(f"❌ {message}")

# MusicSynth cleanup section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🧹 Clean Up Files", use_container_width=True, type="secondary"):
        st.session_state.file_processor.cleanup()
        st.success("✨ Files cleaned up successfully!")

# MusicSynth about section
st.markdown("---")
st.markdown("""
<div class="musicsynth-card">
    <h3 style="margin: 0 0 1rem 0; color: var(--foreground);">🎼 About MusicSynth</h3>
    <p style="margin: 0 0 1rem 0; color: var(--foreground);">
        MusicSynth revolutionizes music education by transforming traditional sheet music into engaging visual experiences. 
        Built with passion by a high school student who believes in making music learning more accessible and exciting for everyone.
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.25rem; margin-top: 1.25rem;">
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">🎹 Desktop Features</h4>
            <ul style="margin: 0; padding-left: 1.25rem; color: var(--muted-foreground); font-size: 0.875rem;">
                <li>Optical Music Recognition</li>
                <li>Sheet music image processing</li>
                <li>Advanced visualization options</li>
                <li>High-quality video export</li>
            </ul>
        </div>
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">☁️ Cloud Features</h4>
            <ul style="margin: 0; padding-left: 1.25rem; color: var(--muted-foreground); font-size: 0.875rem;">
                <li>MusicXML processing</li>
                <li>Secure user authentication</li>
                <li>Cross-platform accessibility</li>
                <li>Real-time collaboration ready</li>
            </ul>
        </div>
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">🎨 Visual Magic</h4>
            <ul style="margin: 0; padding-left: 1.25rem; color: var(--muted-foreground); font-size: 0.875rem;">
                <li>Piano roll animations</li>
                <li>Beautiful color schemes</li>
                <li>Smooth visual transitions</li>
                <li>Educational focus</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Developer note
st.markdown("""
<div class="developer-note">
    <h4>Built with Passion ❤️</h4>
    <p>Created by a passionate high school student dedicated to revolutionizing music education through technology</p>
</div>
""", unsafe_allow_html=True)



# Close the centered container
st.markdown('</div>', unsafe_allow_html=True)