import axios from 'axios';
import config from '../../config';

class ModalApiService {
  constructor() {
    this.apiUrl = config.MODAL_API_URL;
    this.healthUrl = config.MODAL_HEALTH_URL;
  }

  // Health check endpoint
  async healthCheck() {
    try {
      const response = await axios.get(this.healthUrl);
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('Health check failed:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // Process music file endpoint
  async processMusicFile(file, onProgress) {
    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        this.apiUrl,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          responseType: 'blob',
          onUploadProgress: (progressEvent) => {
            if (onProgress) {
              const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              onProgress(percentCompleted);
            }
          },
        }
      );

      // Create video URL from blob
      const videoBlob = new Blob([response.data], { type: 'video/mp4' });
      const videoURL = URL.createObjectURL(videoBlob);
      
      // Extract filename from response headers
      const contentDisposition = response.headers['content-disposition'];
      let filename = 'music_visualization.mp4';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch) {
          filename = filenameMatch[1];
        }
      }

      return {
        success: true,
        videoUrl: videoURL,
        filename: filename,
        data: response.data
      };

    } catch (error) {
      console.error('Process music file failed:', error);
      
      // Handle different error types
      if (error.name === 'CanceledError') {
        return {
          success: false,
          error: 'Upload cancelled',
          type: 'cancelled'
        };
      } else if (error.code === 'ERR_NETWORK') {
        return {
          success: false,
          error: `Network error: ${error.message}. Please check your internet connection.`,
          type: 'network'
        };
      } else if (error.response?.status === 404) {
        return {
          success: false,
          error: 'API endpoint not found. Please check the Modal API URL configuration.',
          type: 'not_found'
        };
      } else if (error.response?.status === 400) {
        return {
          success: false,
          error: 'Invalid file format. Please upload a MusicXML file or image.',
          type: 'bad_request'
        };
      } else if (error.response?.status === 500) {
        return {
          success: false,
          error: 'Server error. Please try again later.',
          type: 'server_error'
        };
      } else {
        return {
          success: false,
          error: `Failed to process file: ${error.message}`,
          type: 'unknown'
        };
      }
    }
  }

  // Test API connection
  async testConnection() {
    try {
      const healthResult = await this.healthCheck();
      if (healthResult.success) {
        return {
          success: true,
          message: 'API connection successful!',
          data: healthResult.data
        };
      } else {
        return {
          success: false,
          message: `Health check failed: ${healthResult.error}`
        };
      }
    } catch (error) {
      return {
        success: false,
        message: `Connection test failed: ${error.message}`
      };
    }
  }
}

export default new ModalApiService(); 