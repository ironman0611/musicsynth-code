import React from 'react';

const ProcessingStatus = ({ status, message, progress, onCancel }) => {
  return (
    <div className="card">
      <h3>⚙️ Creating Magic</h3>
      <p>Converting your music into a stunning visual experience</p>
      
      <div className="processing">
        <div className="spinner"></div>
        <h3>{message}</h3>
        
        {status === 'uploading' && (
          <div style={{ marginTop: '1rem' }}>
            <div style={{ 
              width: '100%', 
              backgroundColor: 'var(--secondary)', 
              borderRadius: 'var(--radius)', 
              overflow: 'hidden',
              marginBottom: '0.5rem'
            }}>
              <div style={{ 
                width: `${progress}%`, 
                height: '8px', 
                backgroundColor: 'var(--primary)', 
                transition: 'width 0.3s ease'
              }}></div>
            </div>
            <div style={{ fontSize: '0.875rem', color: 'var(--muted-foreground)' }}>
              {progress}% uploaded
            </div>
          </div>
        )}
        
        {status === 'processing' && (
          <div style={{ marginTop: '1rem' }}>
            <div style={{ fontSize: '0.875rem', color: 'var(--muted-foreground)' }}>
              🎼 Analyzing your music...
              <br />
              🎨 Generating visual elements...
              <br />
              🎬 Creating video...
            </div>
          </div>
        )}
        
        <div style={{ marginTop: '2rem' }}>
          <button onClick={onCancel} className="button destructive">
            ❌ Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProcessingStatus; 