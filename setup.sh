#!/bin/bash

# MusicSynth Setup Script
# This script helps set up the MusicSynth distributed architecture

echo "🎵 MusicSynth Setup Script"
echo "=========================="

# Check if we're in the right directory
if [ ! -f "setup.sh" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed"
    exit 1
fi

if ! command_exists git; then
    echo "❌ git is required but not installed"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Modal backend
echo ""
echo "🔧 Setting up Modal backend..."

if ! command_exists modal; then
    echo "📦 Installing Modal..."
    pip install modal
fi

cd modal_backend

echo "📦 Installing Modal backend dependencies..."
pip install -r requirements.txt

echo "🔑 Setting up Modal token..."
echo "Please run 'modal token new' to authenticate with Modal"
echo "Press Enter to continue after authentication..."
read

echo "🚀 Deploying to Modal..."
python deploy.py

cd ..

# Setup React frontend
echo ""
echo "⚛️ Setting up React frontend..."

cd frontend

echo "📦 Installing frontend dependencies..."
npm install

echo "🔧 Setting up environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Supabase Configuration
REACT_APP_SUPABASE_URL=your_supabase_project_url
REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key

# Modal API Configuration
REACT_APP_MODAL_API_URL=https://your-modal-deployment.modal.run
EOF
    echo "📝 Created .env file. Please edit it with your actual values."
else
    echo "✅ .env file already exists"
fi

echo "🔧 Building frontend..."
npm run build

cd ..

# Final instructions
echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set up your Supabase project at https://supabase.com"
echo "2. Update the .env file in the frontend directory with your credentials"
echo "3. Create a GitHub repository and push your code"
echo "4. Configure GitHub Pages and GitHub Actions"
echo "5. Test the full system"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
echo "🎵 Happy music synthesizing!" 