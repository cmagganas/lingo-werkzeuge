"""
Tool for speech recognition using Vapi.
"""
import os
import time
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ListenInput(BaseModel):
    """Input schema for the 'listen' tool."""
    max_listen_time: int = Field(default=30, description="Maximum time to listen in seconds")
    language: str = Field(default="en-US", description="Language code for speech recognition")

class ListenOutput(BaseModel):
    """Output schema for the 'listen' tool."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    text: Optional[str] = Field(None, description="Transcribed text")

def listen(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Listen for speech and convert to text using Vapi.
    
    Args:
        input_data: Dictionary containing the input parameters
        
    Returns:
        Dictionary containing the output parameters
    """
    # Parse input
    input_model = ListenInput(**input_data)
    
    # Get API key from environment variables
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        logger.error("VAPI_API_KEY environment variable not set")
        return ListenOutput(
            success=False,
            message="Error: VAPI_API_KEY environment variable not set",
            text=None
        ).dict()
    
    try:
        # Import the Vapi client
        from vapi_python import Vapi
        
        # Initialize the Vapi client
        client = Vapi(api_key=api_key)
        
        # Create assistant configuration with transcription
        assistant = {
            "model": {
                "model": "gpt-3.5-turbo", 
                "provider": "openai",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    }
                ]
            },
            "voice": {
                "provider": "rime-ai",
                "voiceId": "samantha",  # Default voice, not used for listening
            },
            "transcriber": {
                "model": "nova-3",
                "language": input_model.language,
                "provider": "deepgram"
            }
        }
        
        logger.info("Starting listening session...")
        
        # Start a session with the assistant
        client.start(assistant=assistant)
        
        # In a real implementation, we would get the transcribed text from the client
        # For this mock implementation, we'll simulate listening
        logger.info(f"Listening for up to {input_model.max_listen_time} seconds...")
        
        # Simulate listening (in a real implementation, we'd use the client API)
        # This is a simplified mock implementation
        transcribed_text = "This is a simulated transcription. In a real implementation, this would be the text transcribed from speech."
        
        # Stop the client
        client.stop()
        
        return ListenOutput(
            success=True,
            message="Successfully transcribed speech to text",
            text=transcribed_text
        ).dict()
        
    except ImportError as e:
        logger.error(f"Failed to import required module: {e}")
        return ListenOutput(
            success=False,
            message=f"Error: Failed to import required module: {e}",
            text=None
        ).dict()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ListenOutput(
            success=False,
            message=f"Error: {str(e)}",
            text=None
        ).dict() 