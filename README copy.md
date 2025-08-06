# 🎵 MusicSynth - Transform Sheet Music into Visual Magic

> Experience the future of music learning with beautiful piano roll animations

MusicSynth is a revolutionary music education platform that transforms traditional sheet music into engaging visual experiences. Built with a modern distributed architecture for scalability and performance.

## ✨ Features

- **🎼 Optical Music Recognition**: Upload sheet music images and watch them transform into digital scores
- **🎹 Visual Piano Roll**: See your music come alive with stunning piano roll animations
- **🎨 Music Visualization**: Create beautiful visual representations of your musical compositions
- **🔐 Secure Authentication**: User accounts with email verification and password reset
- **☁️ Cloud Processing**: Serverless GPU-powered processing for fast video generation
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

MusicSynth uses a modern distributed architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Pages  │    │    Supabase     │    │     Modal       │
│   (Frontend)    │◄──►│ (Authentication)│    │   (Backend)     │
│                 │    │                 │    │                 │
│ React App       │    │ User Auth       │    │ GPU Processing  │
│ File Upload     │    │ Session Mgmt    │    │ Video Gen       │
│ UI/UX           │    │ Password Reset  │    │ REST API        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Components

- **Frontend**: React application deployed on GitHub Pages
- **Backend**: Modal serverless API with GPU processing capabilities
- **Authentication**: Supabase for secure user management
- **Processing**: GPU-accelerated video generation using Oemer OCR and MoviePy

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+ for Modal backend
- Supabase account
- Modal account
- GitHub account

### Automated Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/musicsynth-code.git
cd musicsynth-code

# Run the setup script
./setup.sh
```

### Manual Setup

1. **Backend (Modal)**:
```bash
   cd modal_backend
pip install -r requirements.txt
   modal token new
   python deploy.py
```

2. **Frontend (React)**:
```bash
   cd frontend
   npm install
   # Configure .env file with your credentials
   npm run build
   ```

3. **Deploy to GitHub Pages**:
   - Push code to GitHub
   - Configure GitHub Secrets
   - Enable GitHub Pages
   - GitHub Actions will handle deployment

## 📖 Documentation

- [**Deployment Guide**](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [**API Documentation**](modal_backend/README.md) - Backend API reference
- [**Frontend Guide**](frontend/README.md) - Frontend development guide

## 🎯 Supported Formats

### Music Files
- `.musicxml` - MusicXML format
- `.xml` - XML music files

### Sheet Music Images
- `.png` - PNG images
- `.jpg` - JPEG images
- `.jpeg` - JPEG images

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern UI framework
- **Supabase**: Authentication and user management
- **Axios**: HTTP client for API requests
- **React Router**: Client-side routing

### Backend
- **Modal**: Serverless GPU computing platform
- **FastAPI**: Modern Python web framework
- **Oemer**: Optical music recognition
- **MoviePy**: Video processing library
- **Pillow**: Image processing

### Infrastructure
- **GitHub Pages**: Static site hosting
- **GitHub Actions**: CI/CD pipeline
- **Supabase**: Backend-as-a-Service
- **Modal**: Serverless compute platform

## 🔐 Security Features

- **Email Verification**: Secure user registration
- **Password Hashing**: Secure password storage
- **JWT Authentication**: Stateless authentication
- **Input Validation**: Server-side validation
- **Rate Limiting**: API protection
- **CORS Configuration**: Cross-origin security

## 📊 Performance

- **GPU Processing**: 3-5x faster video generation
- **Serverless Scaling**: Automatic scaling based on demand
- **CDN Delivery**: Fast global content delivery
- **Optimized Images**: Compressed assets for faster loading

## 🎨 Design System

MusicSynth uses a modern dark theme inspired by shadcn/ui:
- **Dark Background**: `#0A0A0A`
- **Card Background**: `#161616`
- **Primary Color**: `#FAFAFA`
- **Accent Colors**: Music-themed color palette

## 🧪 Testing

### Local Testing
```bash
# Test backend
cd modal_backend
python -m pytest tests/

# Test frontend
cd frontend
npm test
```

### End-to-End Testing
1. Upload a MusicXML file
2. Verify authentication flow
3. Test video generation
4. Validate download functionality

## 🚀 Deployment

### Production Deployment
1. **Modal Backend**: Automatic scaling, GPU instances
2. **GitHub Pages**: CDN-backed static hosting
3. **Supabase**: Managed database and auth

### Cost Optimization
- **Pay-per-use**: Only pay for processing time
- **Free tiers**: Leverages free tiers of all services
- **Automatic scaling**: No idle server costs

## 📈 Monitoring

- **Modal Dashboard**: Backend performance and logs
- **Supabase Dashboard**: User activity and database metrics
- **GitHub Actions**: Build and deployment status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎵 About

MusicSynth was created with passion by a high school student who believes in making music education more accessible and exciting for everyone. The project demonstrates how modern web technologies can transform traditional music education.

## 🆘 Support

- **Documentation**: Check the [Deployment Guide](DEPLOYMENT_GUIDE.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/musicsynth-code/issues)
- **Discussions**: Join the [GitHub Discussions](https://github.com/yourusername/musicsynth-code/discussions)

## 🙏 Acknowledgments

- **Oemer**: For optical music recognition
- **MoviePy**: For video processing
- **Supabase**: For authentication infrastructure
- **Modal**: For serverless GPU computing
- **React**: For the frontend framework

---

<div align="center">
  <strong>🎼 Transform • 🎨 Visualize • 🚀 Learn</strong>
  <br>
  <em>Built with React, Supabase, Modal, and ❤️</em>
</div>
