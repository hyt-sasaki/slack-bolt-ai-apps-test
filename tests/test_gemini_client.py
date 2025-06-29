"""
Tests for Gemini VertexAI client
"""

import pytest
from unittest.mock import Mock, patch
from app.gemini_client import GeminiClient


class TestGeminiClient:
    """Test cases for GeminiClient"""
    
    def test_init_without_google_cloud(self):
        """Test initialization when Google Cloud SDK is not available"""
        with patch('app.gemini_client.aiplatform', None):
            client = GeminiClient("test-project", "us-central1")
            assert client.project_id == "test-project"
            assert client.location == "us-central1"
            assert client.model is None
            assert not client.is_available()
    
    @patch('app.gemini_client.aiplatform')
    @patch('app.gemini_client.generative_models')
    def test_init_with_google_cloud(self, mock_generative_models, mock_aiplatform):
        """Test successful initialization with Google Cloud SDK"""
        mock_model = Mock()
        mock_generative_models.GenerativeModel.return_value = mock_model
        
        client = GeminiClient("test-project", "us-central1", "gemini-1.5-flash")
        
        mock_aiplatform.init.assert_called_once_with(
            project="test-project", 
            location="us-central1"
        )
        mock_generative_models.GenerativeModel.assert_called_once_with("gemini-1.5-flash")
        assert client.model == mock_model
        assert client.is_available()
    
    def test_generate_response_unavailable(self):
        """Test response generation when service is unavailable"""
        client = GeminiClient("test-project", "us-central1")
        client.model = None
        
        response = client.generate_response("Hello")
        assert response == "Sorry, the AI service is currently unavailable."
    
    @patch('app.gemini_client.aiplatform')
    @patch('app.gemini_client.generative_models')
    def test_generate_response_success(self, mock_generative_models, mock_aiplatform):
        """Test successful response generation"""
        # Setup mocks
        mock_response = Mock()
        mock_response.text = "Hello! How can I help you?"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_generative_models.GenerativeModel.return_value = mock_model
        
        # Test
        client = GeminiClient("test-project", "us-central1")
        response = client.generate_response("Hello")
        
        assert response == "Hello! How can I help you?"
        mock_model.generate_content.assert_called_once()
    
    @patch('app.gemini_client.aiplatform')
    @patch('app.gemini_client.generative_models')
    def test_generate_response_empty(self, mock_generative_models, mock_aiplatform):
        """Test handling of empty response"""
        # Setup mocks
        mock_response = Mock()
        mock_response.text = None
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_generative_models.GenerativeModel.return_value = mock_model
        
        # Test
        client = GeminiClient("test-project", "us-central1")
        response = client.generate_response("Hello")
        
        assert "couldn't generate a response" in response
    
    @patch('app.gemini_client.aiplatform')
    @patch('app.gemini_client.generative_models')
    def test_generate_response_exception(self, mock_generative_models, mock_aiplatform):
        """Test handling of exceptions during response generation"""
        # Setup mocks
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_generative_models.GenerativeModel.return_value = mock_model
        
        # Test
        client = GeminiClient("test-project", "us-central1")
        response = client.generate_response("Hello")
        
        assert "encountered an error" in response
    
    @patch('app.gemini_client.aiplatform')
    @patch('app.gemini_client.generative_models')
    def test_generate_streaming_response(self, mock_generative_models, mock_aiplatform):
        """Test streaming response generation"""
        # Setup mocks
        mock_chunk1 = Mock()
        mock_chunk1.text = "Hello "
        mock_chunk2 = Mock()
        mock_chunk2.text = "there!"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = [mock_chunk1, mock_chunk2]
        mock_generative_models.GenerativeModel.return_value = mock_model
        
        # Test
        client = GeminiClient("test-project", "us-central1")
        chunks = list(client.generate_streaming_response("Hello"))
        
        assert chunks == ["Hello ", "there!"]
        mock_model.generate_content.assert_called_once()
        
        # Check that stream=True was passed
        call_args = mock_model.generate_content.call_args
        assert call_args[1]['stream'] is True