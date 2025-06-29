"""
Slack AI Chatbot using Gemini on VertexAI

This is the main application file that sets up the Slack Bolt app
and integrates with Gemini on VertexAI for AI-powered conversations.
"""

import os
import logging
from typing import Dict, Any

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from app.gemini_client import GeminiClient
from listeners.message_listener import register_message_listeners

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Slack Bolt app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize Gemini client
gemini_client = GeminiClient(
    project_id=os.environ.get("GCP_PROJECT_ID"),
    location=os.environ.get("VERTEX_AI_LOCATION", "us-central1"),
    model_name=os.environ.get("VERTEX_AI_MODEL", "gemini-1.5-flash")
)

# Store gemini client in app context for access in listeners
app.client.gemini = gemini_client

# Register message listeners
register_message_listeners(app)

@app.event("app_mention")
def handle_app_mention(event: Dict[str, Any], say, logger):
    """Handle app mentions in channels"""
    try:
        user_message = event["text"]
        # Remove the bot mention from the message
        user_message = user_message.split(">", 1)[-1].strip()
        
        if not user_message:
            say("Hello! How can I help you today?")
            return
        
        # Generate response using Gemini
        response = gemini_client.generate_response(user_message)
        say(response)
        
    except Exception as e:
        logger.error(f"Error handling app mention: {e}")
        say("Sorry, I encountered an error processing your request.")

@app.event("message")
def handle_direct_message(event: Dict[str, Any], say, logger):
    """Handle direct messages to the bot"""
    # Only respond to direct messages (not channel messages)
    if event.get("channel_type") != "im":
        return
    
    try:
        user_message = event.get("text", "")
        
        if not user_message:
            say("Hello! How can I help you today?")
            return
        
        # Generate response using Gemini
        response = gemini_client.generate_response(user_message)
        say(response)
        
    except Exception as e:
        logger.error(f"Error handling direct message: {e}")
        say("Sorry, I encountered an error processing your request.")

@app.route("/health")
def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "gemini_available": gemini_client.is_available()}

def main():
    """Main function to start the Slack app"""
    try:
        # Check if Gemini client is available
        if not gemini_client.is_available():
            logger.warning("Gemini client is not available. Check your Google Cloud configuration.")
        
        # Start the app using Socket Mode for development
        if os.environ.get("SLACK_APP_TOKEN"):
            handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
            logger.info("Starting Slack app in Socket Mode...")
            handler.start()
        else:
            # For production deployment (e.g., Cloud Run)
            port = int(os.environ.get("PORT", 3000))
            logger.info(f"Starting Slack app on port {port}...")
            app.start(port=port)
            
    except KeyboardInterrupt:
        logger.info("App stopped by user")
    except Exception as e:
        logger.error(f"Error starting app: {e}")
        raise

if __name__ == "__main__":
    main()