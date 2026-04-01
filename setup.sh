#!/bin/bash
# Quick start script for Burp Suite AI Agent

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Burp Suite AI Agent - Quick Setup                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
if pip install -r requirements.txt > /dev/null 2>&1; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env configuration file..."
    cp .env.example .env
    echo "✓ .env file created (customize with your Burp Suite connection details)"
else
    echo "ℹ️  .env file already exists"
fi
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║   Setup Complete!                                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To start the agent, run:"
echo "   python agent.py"
echo ""
echo "📚 For examples, run:"
echo "   python examples.py"
echo ""
echo "🧪 To run tests, run:"
echo "   python -m pytest test_agent.py"
echo ""
echo "❓ For help, type 'help' after starting the agent"
