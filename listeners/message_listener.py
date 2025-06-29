"""
Message listeners for the Slack AI chatbot

This module contains listeners for various message events and patterns.
"""

import logging
from typing import Dict, Any
from slack_bolt import App

logger = logging.getLogger(__name__)

def register_message_listeners(app: App):
    """Register all message-related listeners"""
    
    @app.message("hello")
    def handle_hello(message: Dict[str, Any], say):
        """Respond to hello messages"""
        user = message.get("user", "there")
        say(f"Hello <@{user}>! I'm an AI assistant powered by Gemini. How can I help you today?")
    
    @app.message("help")
    def handle_help(message: Dict[str, Any], say):
        """Provide help information"""
        help_text = """
🤖 *AI Chatbot Help*

I'm an AI assistant powered by Google's Gemini model. Here's how to interact with me:

*Direct Messages:*
• Send me a direct message with any question or request
• I'll respond with AI-generated answers

*In Channels:*
• Mention me (@botname) followed by your message
• I'll respond in the channel thread

*Examples:*
• "What is the weather like today?"
• "Help me write a Python function"
• "Explain quantum computing"
• "Tell me a joke"

*Commands:*
• `hello` - Get a greeting
• `help` - Show this help message

Feel free to ask me anything! 🚀
        """
        say(help_text)
    
    @app.message("ping")
    def handle_ping(message: Dict[str, Any], say):
        """Respond to ping with pong"""
        say("🏓 Pong! I'm alive and ready to help!")
    
    logger.info("Message listeners registered successfully")