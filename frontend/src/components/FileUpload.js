import React, { useState, useRef } from 'react';

const FileUpload = ({ onFileUpload }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const supportedFormats = [
    'musicxml', 'xml', 'png', 'jpg', 'jpeg'
  ];

  const isFileSupported = (file) => {
    const extension = file.name.split('.').pop().toLowerCase();
    return supportedFormats.includes(extension);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileSelection = (file) => {
    if (!isFileSupported(file)) {
      alert('Please select a supported file format (.musicxml, .xml, .png, .jpg, .jpeg)');
      return;
    }

    // Check file size (limit to 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return;
    }

    setSelectedFile(file);
  };

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelection(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onFileUpload(selectedFile);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div>
      <div
        className={`file-upload ${isDragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="file-upload-icon">
          {selectedFile ? '📁' : '📤'}
        </div>
        
        {selectedFile ? (
          <div>
            <div className="file-upload-text">
              File Selected: {selectedFile.name}
            </div>
            <div className="file-upload-hint">
              Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </div>
          </div>
        ) : (
          <div>
            <div className="file-upload-text">
              {isDragOver ? 'Drop your file here' : 'Click to upload or drag and drop'}
            </div>
            <div className="file-upload-hint">
              Supports: .musicxml, .xml, .png, .jpg, .jpeg (Max 10MB)
            </div>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept=".musicxml,.xml,.png,.jpg,.jpeg"
        onChange={handleFileInputChange}
        style={{ display: 'none' }}
      />

      {selectedFile && (
        <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <button onClick={handleUpload} className="button">
            🚀 Process File
          </button>
          <button onClick={handleClear} className="button secondary">
            ✖️ Clear
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload; 