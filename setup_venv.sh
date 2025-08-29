#!/bin/bash

# Sister API Client - Virtual Environment Setup Script

echo "🐍 Setting up Sister API Client virtual environment..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your Sister credentials"
    echo "   Required variables:"
    echo "   - SISTER_URL"
    echo "   - SISTER_USERNAME"
    echo "   - SISTER_PASSWORD"
    echo "   - SISTER_ID_PENGGUNA"
else
    echo "✅ .env file already exists"
fi

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
python test_fixes.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future:"
echo "   source venv/bin/activate"
echo ""
echo "To deactivate:"
echo "   deactivate"
echo ""
echo "To run the Sister API client:"
echo "   python sister.py"
echo ""
echo "To manage cache:"
echo "   python cache_manager.py --help"
