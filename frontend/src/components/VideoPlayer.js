import React from 'react';

const VideoPlayer = ({ videoUrl, filename, onDownload, onReset }) => {
  return (
    <div className="card">
      <h3>🎥 Your Musical Magic</h3>
      <p>Your sheet music has been transformed into a beautiful visual piano roll animation</p>
      
      <div className="video-container">
        <video
          src={videoUrl}
          controls
          style={{
            width: '100%',
            maxWidth: '800px',
            height: 'auto',
            borderRadius: 'var(--radius)',
            border: '1px solid var(--border)'
          }}
        >
          Your browser does not support the video tag.
        </video>
      </div>
      
      <div className="download-section">
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button onClick={onDownload} className="button">
            ⬇️ Download Your Creation
          </button>
          <button onClick={onReset} className="button secondary">
            🔄 Process Another File
          </button>
        </div>
        
        <div style={{ marginTop: '1rem', color: 'var(--muted-foreground)', fontSize: '0.875rem' }}>
          <strong>Filename:</strong> {filename}
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer; 