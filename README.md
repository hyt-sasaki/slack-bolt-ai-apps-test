# Slack AI Chatbot with Gemini on VertexAI

A Slack AI chatbot prototype built with Slack Bolt for Python and Google's Gemini model on VertexAI.

## Features

- 🤖 AI-powered conversations using Google Gemini
- 💬 Direct message support
- 📢 Channel mention responses
- 🚀 Cloud Run deployment ready
- 🛠️ Modern Python tooling with mise and uv
- 🔧 Slack CLI 3.x integration

## Architecture

- **Framework**: Slack Bolt for Python
- **AI Model**: Google Gemini on VertexAI
- **Deployment**: Google Cloud Run
- **Tool Management**: mise
- **Package Management**: uv
- **Slack Management**: Slack CLI 3.x

## Prerequisites

- Python 3.8+
- Google Cloud Platform account
- Slack workspace with admin permissions
- mise (optional, for tool management)

## Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd slack-bolt-ai-apps-test

# Run setup script (installs tools and dependencies)
./setup.sh

# Or manual setup:
pip install -e ".[dev]"
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your actual values:

```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_APP_TOKEN=xapp-your-slack-app-token
SLACK_SIGNING_SECRET=your-slack-signing-secret

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1

# Vertex AI Configuration
VERTEX_AI_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-1.5-flash
```

### 3. Google Cloud Setup

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create service account for VertexAI
gcloud iam service-accounts create slack-ai-chatbot
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:slack-ai-chatbot@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Download service account key
gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=slack-ai-chatbot@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### 4. Slack App Setup

Using Slack CLI 3.x:

```bash
# Create new Slack app from manifest
slack create app --manifest manifest.yaml

# Or create from template
slack create app --template https://github.com/slack-samples/bolt-python-ai-chatbot

# Install the app to your workspace
slack install app
```

### 5. Run the Application

For development (Socket Mode):
```bash
python main.py
```

For production deployment:
```bash
./deploy.sh
```

## Development

### Project Structure

```
slack-bolt-ai-apps-test/
├── app/
│   ├── __init__.py
│   └── gemini_client.py      # VertexAI Gemini integration
├── listeners/
│   ├── __init__.py
│   └── message_listener.py   # Slack event listeners
├── tests/                    # Test files
├── main.py                   # Main application entry point
├── manifest.yaml             # Slack app manifest
├── Dockerfile               # Container configuration
├── deploy.sh                # Cloud Run deployment script
├── setup.sh                 # Development environment setup
├── pyproject.toml           # Python project configuration
├── .mise.toml               # Tool configuration
└── .env.example             # Environment template
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov=listeners

# Run specific test file
pytest tests/test_gemini_client.py
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8

# Type checking
mypy .
```

## Deployment

### Cloud Run Deployment

1. **Build and Deploy**:
   ```bash
   ./deploy.sh
   ```

2. **Set Environment Variables**:
   ```bash
   gcloud run services update slack-ai-chatbot \
     --region=us-central1 \
     --set-env-vars="SLACK_BOT_TOKEN=xoxb-..." \
     --set-env-vars="SLACK_SIGNING_SECRET=..." \
     --set-env-vars="GCP_PROJECT_ID=your-project-id"
   ```

3. **Update Slack App Configuration**:
   - Set Request URL to: `https://your-service-url.run.app/slack/events`
   - Disable Socket Mode for production

### Using mise for Tool Management

```bash
# Install all tools
mise install

# Use specific Slack CLI version
mise use "aqua:slack.com/slack-cli@3.4.0"

# Update tools
mise upgrade
```

## Usage

### Bot Commands

- **hello** - Get a greeting message
- **help** - Show help information
- **ping** - Check if bot is alive

### Interaction Modes

1. **Direct Messages**: Send any message directly to the bot
2. **Channel Mentions**: Mention the bot in channels with `@botname your message`

### Example Conversations

```
User: @ai-chatbot What is Python?
Bot: Python is a high-level, interpreted programming language...

User: Help me write a function to calculate fibonacci
Bot: Here's a Python function to calculate Fibonacci numbers...
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Bot user OAuth token | Required |
| `SLACK_APP_TOKEN` | App-level token for Socket Mode | Required for dev |
| `SLACK_SIGNING_SECRET` | Slack app signing secret | Required |
| `GCP_PROJECT_ID` | Google Cloud project ID | Required |
| `VERTEX_AI_LOCATION` | VertexAI region | `us-central1` |
| `VERTEX_AI_MODEL` | Gemini model name | `gemini-1.5-flash` |
| `PORT` | Application port | `3000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Slack App Manifest

The `manifest.yaml` file configures:
- Bot permissions and scopes
- Event subscriptions
- OAuth settings
- App display information

## Troubleshooting

### Common Issues

1. **Import Error for Google Cloud**:
   ```bash
   pip install google-cloud-aiplatform
   ```

2. **Authentication Issues**:
   ```bash
   gcloud auth application-default login
   ```

3. **Slack Token Issues**:
   - Verify tokens in Slack app settings
   - Check token permissions and scopes

### Logs

View application logs:
```bash
# Local development
python main.py

# Cloud Run
gcloud logs read --service=slack-ai-chatbot
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
