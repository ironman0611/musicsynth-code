#!/bin/bash

# MusicSynth Modal Deployment Script

echo "🚀 Deploying MusicSynth API to Modal..."
echo "========================================"

# Check if Modal is installed
if ! python3 -c "import modal" 2>/dev/null; then
    echo "❌ Modal is not installed. Installing..."
    pip install modal
fi

# Check if user is authenticated with Modal
echo "🔐 Checking Modal authentication..."
if ! modal token list 2>/dev/null | grep -q "ACTIVE"; then
    echo "❌ Not authenticated with Modal. Please run:"
    echo "   modal token new"
    echo "Then run this script again."
    exit 1
fi

echo "✅ Modal authentication verified"

# Deploy the API
echo "📦 Deploying API to Modal..."
echo "This may take a few minutes..."

python3 modal_api_server.py

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "Your Modal endpoints are now available at:"
echo "- Health check: https://your-app--health.modal.run"
echo "- Process image: https://your-app--process-image.modal.run"
echo "- Process MusicXML: https://your-app--process-musicxml.modal.run"
echo ""
echo "To test the deployment, update the MODAL_BASE_URL in test_modal_api.py"
echo "and run: python3 test_modal_api.py"
echo ""
echo "For more information, see MODAL_DEPLOYMENT_GUIDE.md" 