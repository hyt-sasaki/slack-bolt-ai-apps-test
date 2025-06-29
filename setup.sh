#!/bin/bash

# Setup script for development environment

echo "🔧 Setting up development environment for Slack AI Chatbot"

# Install mise if not available
if ! command -v mise &> /dev/null; then
    echo "📦 Installing mise..."
    curl https://mise.run | sh
    echo 'eval "$(mise activate bash)"' >> ~/.bashrc
    source ~/.bashrc
fi

# Install tools using mise
echo "🛠️ Installing development tools with mise..."
mise install

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
if command -v uv &> /dev/null; then
    uv sync
else
    pip install -e ".[dev]"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your actual configuration values"
fi

# Install Slack CLI if not available
if ! command -v slack &> /dev/null; then
    echo "📱 Installing Slack CLI..."
    mise use "aqua:slack.com/slack-cli@3.4.0"
fi

echo "✅ Development environment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update .env with your Slack app credentials"
echo "2. Set up Google Cloud credentials"
echo "3. Run 'python main.py' to start the app"
echo "4. Use 'slack create app' to create a new Slack app from the template"