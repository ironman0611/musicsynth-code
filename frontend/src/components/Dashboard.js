import React, { useState, useRef } from 'react';
import FileUpload from './FileUpload';
import VideoPlayer from './VideoPlayer';
import ProcessingStatus from './ProcessingStatus';
import modalApiService from '../services/modalApi';

const Dashboard = ({ user, signOut }) => {
  const [processingStatus, setProcessingStatus] = useState('idle'); // idle, uploading, processing, completed, error
  const [message, setMessage] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [videoFilename, setVideoFilename] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const abortController = useRef(null);

  // Modal API configuration
  const MODAL_API_URL = process.env.REACT_APP_MODAL_API_URL || 'https://cotoyota09--musicsynth-backend-process-music-file.modal.run';

  const handleFileUpload = async (file) => {
    if (!file) return;

    // Reset state
    setProcessingStatus('uploading');
    setMessage('Uploading file...');
    setVideoUrl('');
    setVideoFilename('');
    setUploadProgress(0);

    // Create abort controller for cancellation
    abortController.current = new AbortController();

    try {
      console.log('Starting file upload...');
      console.log('File details:', {
        name: file.name,
        size: file.size,
        type: file.type
      });

      // Use Modal API service
      const result = await modalApiService.processMusicFile(
        file,
        (progress) => {
          setUploadProgress(progress);
          console.log('Upload progress:', progress + '%');
          
          if (progress === 100) {
            setProcessingStatus('processing');
            setMessage('Processing your music file...');
          }
        }
      );

      if (result.success) {
        setVideoUrl(result.videoUrl);
        setVideoFilename(result.filename);
        setProcessingStatus('completed');
        setMessage('Video generated successfully!');
      } else {
        throw new Error(result.error);
      }

    } catch (error) {
      console.error('Error details:', {
        name: error.name,
        message: error.message,
        code: error.code
      });

      setProcessingStatus('error');
      setMessage(error.message || 'Failed to process file. Please try again.');
    }
  };

  const handleCancel = () => {
    if (abortController.current) {
      abortController.current.abort();
    }
  };

  const handleReset = () => {
    setProcessingStatus('idle');
    setMessage('');
    setVideoUrl('');
    setVideoFilename('');
    setUploadProgress(0);
    if (videoUrl) {
      URL.revokeObjectURL(videoUrl);
    }
  };

  const downloadVideo = () => {
    if (videoUrl && videoFilename) {
      const link = document.createElement('a');
      link.href = videoUrl;
      link.download = videoFilename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="fade-in">
      {/* Header */}
      <div className="header">
        <h1>🎵 MusicSynth</h1>
        <p>Transform Sheet Music into Visual Magic</p>
        <p className="tagline">Experience the future of music learning</p>
      </div>

      {/* User Menu */}
      <div className="user-menu">
        <div className="user-info">
          <span>🎵 Welcome!</span>
          <div className="user-email">{user.email}</div>
        </div>
        <button onClick={signOut} className="button secondary">
          🚪 Sign Out
        </button>
      </div>

      {/* Features Grid */}
      <div className="feature-grid">
        <div className="feature-item">
          <div className="feature-icon">🎼</div>
          <div className="feature-title">Optical Music Recognition</div>
          <div className="feature-description">Upload sheet music images and watch them transform into digital scores</div>
        </div>
        <div className="feature-item">
          <div className="feature-icon">🎹</div>
          <div className="feature-title">Visual Piano Roll</div>
          <div className="feature-description">See your music come alive with stunning piano roll animations</div>
        </div>
        <div className="feature-item">
          <div className="feature-icon">🎨</div>
          <div className="feature-title">Music Visualization</div>
          <div className="feature-description">Create beautiful visual representations of your musical compositions</div>
        </div>
      </div>

      {/* File Upload Section */}
      {processingStatus === 'idle' && (
        <div className="card">
          <h3>📁 Upload Your Music</h3>
          <p>Choose a MusicXML file or upload a sheet music image to begin the transformation</p>
          <FileUpload onFileUpload={handleFileUpload} />
        </div>
      )}

      {/* Processing Status */}
      {(processingStatus === 'uploading' || processingStatus === 'processing') && (
        <ProcessingStatus 
          status={processingStatus}
          message={message}
          progress={uploadProgress}
          onCancel={handleCancel}
        />
      )}

      {/* Video Result */}
      {processingStatus === 'completed' && videoUrl && (
        <VideoPlayer 
          videoUrl={videoUrl}
          filename={videoFilename}
          onDownload={downloadVideo}
          onReset={handleReset}
        />
      )}

      {/* Error State */}
      {processingStatus === 'error' && (
        <div className="card">
          <h3>❌ Processing Error</h3>
          <div className="alert error">
            {message}
          </div>
          <button onClick={handleReset} className="button">
            Try Again
          </button>
        </div>
      )}

      {/* Debug Section - Remove in production */}
      <div className="card" style={{ backgroundColor: '#f0f0f0', border: '1px solid #ccc' }}>
        <h3>🔧 Debug Information</h3>
        <p><strong>Modal API URL:</strong> {MODAL_API_URL}</p>
        <p><strong>Environment:</strong> {process.env.NODE_ENV}</p>
        <button 
          onClick={async () => {
            try {
              console.log('Testing API connection...');
              const result = await modalApiService.testConnection();
              if (result.success) {
                console.log('Health check response:', result.data);
                alert('API connection successful!');
              } else {
                alert(`API connection failed: ${result.message}`);
              }
            } catch (error) {
              console.error('Health check failed:', error);
              alert(`API connection failed: ${error.message}`);
            }
          }}
          className="button secondary"
          style={{ marginRight: '10px' }}
        >
          Test API Connection
        </button>
        <button 
          onClick={() => {
            console.log('Current environment variables:', {
              REACT_APP_SUPABASE_URL: process.env.REACT_APP_SUPABASE_URL,
              REACT_APP_SUPABASE_ANON_KEY: process.env.REACT_APP_SUPABASE_ANON_KEY,
              REACT_APP_MODAL_API_URL: process.env.REACT_APP_MODAL_API_URL
            });
            alert('Check console for environment variables');
          }}
          className="button secondary"
        >
          Show Environment Variables
        </button>
      </div>

      {/* How to Use */}
      <div className="card">
        <h3>🚀 How to Use</h3>
        <ol style={{ paddingLeft: '1.5rem', color: 'var(--muted-foreground)' }}>
          <li>Upload your MusicXML file or sheet music image</li>
          <li>Watch the magic happen as we process your music</li>
          <li>Preview your beautiful piano roll visualization</li>
          <li>Download your creation to share with others</li>
        </ol>
      </div>

      {/* Supported Formats */}
      <div className="card">
        <h3>📄 Supported Formats</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div>
            <strong>🎼 Music Files:</strong>
            <br />
            <code style={{ backgroundColor: 'var(--muted)', padding: '0.25rem', borderRadius: '0.25rem', fontSize: '0.75rem' }}>
              .musicxml
            </code>{' '}
            <code style={{ backgroundColor: 'var(--muted)', padding: '0.25rem', borderRadius: '0.25rem', fontSize: '0.75rem' }}>
              .xml
            </code>
          </div>
          <div>
            <strong>📷 Sheet Music Images:</strong>
            <br />
            <code style={{ backgroundColor: 'var(--muted)', padding: '0.25rem', borderRadius: '0.25rem', fontSize: '0.75rem' }}>
              .png
            </code>{' '}
            <code style={{ backgroundColor: 'var(--muted)', padding: '0.25rem', borderRadius: '0.25rem', fontSize: '0.75rem' }}>
              .jpg
            </code>{' '}
            <code style={{ backgroundColor: 'var(--muted)', padding: '0.25rem', borderRadius: '0.25rem', fontSize: '0.75rem' }}>
              .jpeg
            </code>
          </div>
        </div>
      </div>

      {/* About Section */}
      <div className="card">
        <h3>🎼 About MusicSynth</h3>
        <p>
          MusicSynth revolutionizes music education by transforming traditional sheet music into engaging visual experiences. 
          Built with passion by a high school student who believes in making music learning more accessible and exciting for everyone.
        </p>
        <div className="feature-grid" style={{ marginTop: '1rem' }}>
          <div>
            <h4>🎹 Key Features</h4>
            <ul style={{ paddingLeft: '1.5rem', color: 'var(--muted-foreground)', fontSize: '0.875rem' }}>
              <li>Optical Music Recognition</li>
              <li>Sheet music image processing</li>
              <li>Advanced visualization options</li>
              <li>High-quality video export</li>
            </ul>
          </div>
          <div>
            <h4>☁️ Cloud Features</h4>
            <ul style={{ paddingLeft: '1.5rem', color: 'var(--muted-foreground)', fontSize: '0.875rem' }}>
              <li>MusicXML processing</li>
              <li>Secure user authentication</li>
              <li>Cross-platform accessibility</li>
              <li>Real-time processing</li>
            </ul>
          </div>
          <div>
            <h4>🎨 Visual Magic</h4>
            <ul style={{ paddingLeft: '1.5rem', color: 'var(--muted-foreground)', fontSize: '0.875rem' }}>
              <li>Piano roll animations</li>
              <li>Beautiful color schemes</li>
              <li>Smooth visual transitions</li>
              <li>Educational focus</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Developer Note */}
      <div className="developer-note">
        <h4>Built with Passion ❤️</h4>
        <p>Created by a passionate high school student dedicated to revolutionizing music education through technology</p>
      </div>

      {/* Footer */}
      <div style={{ textAlign: 'center', padding: '24px', opacity: 0.7 }}>
        <p style={{ margin: '0', fontSize: '0.9rem' }}>
          🎼 <strong>Transform</strong> • 🎨 <strong>Visualize</strong> • 🚀 <strong>Learn</strong>
        </p>
        <p style={{ margin: '8px 0 0 0', fontSize: '0.8rem', opacity: 0.6 }}>
          Built with React, Supabase, Modal, and ❤️
        </p>
      </div>
    </div>
  );
};

export default Dashboard; 