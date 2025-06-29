"""
Gemini VertexAI Client

This module provides a client for interacting with Google's Gemini model
on VertexAI for generating AI responses.
"""

import logging
from typing import Optional, List, Dict, Any

try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform import generative_models
except ImportError:
    # Graceful handling for development without Google Cloud SDK
    aiplatform = None
    generative_models = None

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini on VertexAI"""
    
    def __init__(self, project_id: str, location: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the Gemini client
        
        Args:
            project_id: Google Cloud project ID
            location: VertexAI location (e.g., 'us-central1')
            model_name: Name of the Gemini model to use
        """
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.model = None
        
        if aiplatform is None:
            logger.warning("Google Cloud AI Platform not available. Install with: pip install google-cloud-aiplatform")
            return
            
        try:
            # Initialize VertexAI
            aiplatform.init(project=project_id, location=location)
            
            # Initialize the generative model
            self.model = generative_models.GenerativeModel(model_name)
            logger.info(f"Initialized Gemini model: {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.model = None
    
    def generate_response(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate a response using Gemini
        
        Args:
            prompt: The input prompt/message
            max_tokens: Maximum number of tokens in the response
            temperature: Temperature for response generation (0.0-1.0)
            
        Returns:
            Generated response text
        """
        if not self.model:
            return "Sorry, the AI service is currently unavailable."
        
        try:
            # Configure generation parameters
            generation_config = generative_models.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=0.95,
                top_k=40
            )
            
            # Safety settings to prevent harmful content
            safety_settings = [
                generative_models.SafetySetting(
                    category=generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                generative_models.SafetySetting(
                    category=generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                generative_models.SafetySetting(
                    category=generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
                generative_models.SafetySetting(
                    category=generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
                ),
            ]
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini")
                return "I'm sorry, I couldn't generate a response to that."
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your request."
    
    def generate_streaming_response(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7):
        """
        Generate a streaming response using Gemini (for future use)
        
        Args:
            prompt: The input prompt/message
            max_tokens: Maximum number of tokens in the response
            temperature: Temperature for response generation (0.0-1.0)
            
        Yields:
            Response chunks as they are generated
        """
        if not self.model:
            yield "Sorry, the AI service is currently unavailable."
            return
        
        try:
            # Configure generation parameters
            generation_config = generative_models.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=0.95,
                top_k=40
            )
            
            # Generate streaming response
            response_stream = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield "Sorry, I encountered an error while processing your request."
    
    def is_available(self) -> bool:
        """Check if the Gemini client is available and properly initialized"""
        return self.model is not None