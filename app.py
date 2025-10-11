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

def load_logo_base64():
    import base64
    try:
        with open("static/logo.jpg", "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Load logo
logo_data = load_logo_base64()
if logo_data:
    logo_src = f"data:image/jpeg;base64,{logo_data}"
    logo_html = f'<img src="{logo_src}" alt="MusicSynth Logo" style="width: 100%; height: 100%; object-fit: contain; border-radius: 50%;">'
else:
    logo_html = '<span style="font-size: 2.5rem; color: white;">🎵</span>'

# MusicSynth header with modern branding
st.markdown(f"""
<div class="modern-header fade-in" style="margin-top: 0 !important; padding-top: 0 !important;">
    <div style="text-align: center; margin-bottom: 1rem; margin-top: 0 !important; padding-top: 0 !important;">
        <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            {logo_html}
        </div>
    </div>
    <h1>MusicSynth</h1>
    <p>Transform Sheet Music into Visual Magic </p>
                <p style="font-size: 1rem; opacity: 0.8; margin-bottom: 2rem; color: var(--muted-foreground); font-style: italic;">
                Experience the future of music learning
            </p>
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
    # Check if this file has already been processed
    file_key = f"processed_{uploaded_file.name}_{uploaded_file.size}"
    
    # Initialize session state for processed files
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = {}
    
    # Initialize modal container (needed for both new and cached processing)
    modal_container = st.empty()
    
    # Check if file is already processed
    if file_key not in st.session_state.processed_files:
        # Initialize timing statistics
        timing_stats = {
            'start_time': time.time(),
            'steps': {}
        }
        
        # Show modal
        modal_container.markdown("""
        <div id="spinner-modal" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            backdrop-filter: blur(5px);
        ">
            <div style="
                background: white;
                padding: 3rem;
                border-radius: 1rem;
                text-align: center;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
                border: 1px solid var(--border);
            ">
                <div style="
                    width: 80px;
                    height: 80px;
                    border: 6px solid #f3f3f3;
                    border-top: 6px solid var(--primary);
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 1.5rem auto;
                "></div>
                <h3 style="margin: 0; color: var(--foreground); font-size: 1.5rem; font-weight: 600;">
                    🎼 Creating your musical visualization...
                </h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--muted-foreground); font-size: 1rem;">
                    Please wait while we process your music
                </p>
            </div>
        </div>
        
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Process the file (timing is tracked internally by FileProcessor)
        success, message, output_path = st.session_state.file_processor.process_uploaded_file(uploaded_file)
        
        # Get timing information from FileProcessor and update timing_stats
        if hasattr(st.session_state.file_processor, 'timing_stats'):
            fp_timing = st.session_state.file_processor.timing_stats
            
            # Use FileProcessor's timing data directly
            timing_stats['steps'] = fp_timing.copy()
            
            # Calculate total time as sum of all steps
            timing_stats['total_time'] = sum(fp_timing.values())
        else:
            timing_stats['steps'] = {'processing': 0.0}
            timing_stats['total_time'] = 0.0
        
        # Store processing results in session state
        st.session_state.processed_files[file_key] = {
            'success': success,
            'message': message,
            'output_path': output_path,
            'timing_stats': timing_stats
        }
    else:
        # Use cached results
        cached_result = st.session_state.processed_files[file_key]
        success = cached_result['success']
        message = cached_result['message']
        output_path = cached_result['output_path']
        timing_stats = cached_result['timing_stats']
        
        # Hide modal for cached results (no processing needed)
        modal_container.empty()
    
    if success:
        st.success(f"✨ {message}")
        
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
        
        # Unified Performance Metrics Section
        st.markdown("""
        <div class="modern-card">
            <h3>📊 Processing Performance</h3>
            <p style="margin: 0.5rem 0 1.5rem 0; color: var(--muted-foreground);">Detailed timing breakdown for all processing steps</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create comprehensive stats display
        stats_data = []
        for step, duration in timing_stats['steps'].items():
            # Format step names nicely
            step_name = step.replace('_', ' ').title()
            stats_data.append([step_name, f"{duration:.2f}s"])
        
        # Add total time
        stats_data.append(['Total Time', f"{timing_stats['total_time']:.2f}s"])
        
        # Display all metrics in a clean grid layout
        if len(stats_data) > 0:
            # Create columns based on number of metrics
            num_cols = min(len(stats_data), 4)  # Max 4 columns
            cols = st.columns(num_cols)
            
            for i, (step, time) in enumerate(stats_data):
                col_idx = i % num_cols
                with cols[col_idx]:
                    # Use different colors for different metric types
                    if step == 'Total Time':
                        color = 'var(--success)'
                        bg_color = 'var(--success)'
                        text_color = 'white'
                    elif step == 'Video Generation':
                        color = 'var(--accent)'
                        bg_color = 'var(--accent)'
                        text_color = 'white'
                    else:
                        color = 'var(--primary)'
                        bg_color = 'var(--muted)'
                        text_color = 'var(--foreground)'
                    
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1.5rem; background: {bg_color}; border-radius: 0.75rem; margin-bottom: 1rem;">
                        <div style="font-size: 2rem; font-weight: 700; color: {text_color};">{time}</div>
                        <div style="font-size: 0.875rem; color: {text_color}; margin-top: 0.5rem; opacity: 0.9;">{step}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
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
        
        # Hide the modal
        modal_container.empty()
    else:
        st.error(f"❌ {message}")
        
        # Hide the modal even if processing failed
        modal_container.empty()

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