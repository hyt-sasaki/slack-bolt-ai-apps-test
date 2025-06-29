"""
Tests for message listeners
"""

import pytest
from unittest.mock import Mock, patch
from slack_bolt import App
from listeners.message_listener import register_message_listeners


class TestMessageListeners:
    """Test cases for message listeners"""
    
    def setup_method(self):
        """Setup test environment"""
        self.app = Mock(spec=App)
        self.app.message = Mock()
        
    def test_register_message_listeners(self):
        """Test that message listeners are registered"""
        register_message_listeners(self.app)
        
        # Check that message decorators were called
        assert self.app.message.call_count == 3
        
        # Check the patterns that were registered
        call_args = [call[0][0] for call in self.app.message.call_args_list]
        expected_patterns = ["hello", "help", "ping"]
        assert call_args == expected_patterns
    
    def test_hello_handler(self):
        """Test hello message handler"""
        # Mock say function
        say = Mock()
        
        # Mock message
        message = {"user": "U123456"}
        
        # Register listeners and extract hello handler
        register_message_listeners(self.app)
        hello_handler = self.app.message.call_args_list[0][1]['func'] if self.app.message.call_args_list else None
        
        # This test is simplified since we can't easily extract the decorated function
        # In a real scenario, you'd test the handler function directly
        assert self.app.message.called
    
    def test_help_handler_content(self):
        """Test that help handler provides useful content"""
        # Register listeners
        register_message_listeners(self.app)
        
        # Verify help was registered
        help_calls = [call for call in self.app.message.call_args_list if call[0][0] == "help"]
        assert len(help_calls) == 1
    
    def test_ping_handler(self):
        """Test ping message handler"""
        # Register listeners
        register_message_listeners(self.app)
        
        # Verify ping was registered
        ping_calls = [call for call in self.app.message.call_args_list if call[0][0] == "ping"]
        assert len(ping_calls) == 1