"""
Tool for converting text to speech using Vapi with Rime AI voices.
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

class SayInput(BaseModel):
    """Input schema for the 'say' tool."""
    text: str = Field(..., description="The text to convert to speech")
    voice_id: str = Field(default="samantha", description="The Rime AI voice ID to use")
    wait_for_completion: bool = Field(default=True, description="Whether to wait for the speech to complete")
    wait_time: int = Field(default=10, description="Time to wait for response in seconds if wait_for_completion is True")

class SayOutput(BaseModel):
    """Output schema for the 'say' tool."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    audio_url: Optional[str] = Field(None, description="URL to the generated audio (if available)")

def say(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert text to speech using Vapi with Rime AI voices.
    
    Args:
        input_data: Dictionary containing the input parameters
        
    Returns:
        Dictionary containing the output parameters
    """
    # Parse input
    input_model = SayInput(**input_data)
    
    # Get API key from environment variables
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        logger.error("VAPI_API_KEY environment variable not set")
        return SayOutput(
            success=False,
            message="Error: VAPI_API_KEY environment variable not set",
            audio_url=None
        ).dict()
    
    try:
        # Import the Vapi client
        from vapi_python import Vapi
        
        # Initialize the Vapi client
        client = Vapi(api_key=api_key)
        
        # Create assistant configuration with Rime AI voice
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
                "voiceId": input_model.voice_id,
            },
            "transcriber": {
                "model": "nova-3",
                "language": "en-US",
                "provider": "deepgram"
            }
        }
        
        logger.info(f"Creating assistant with voice: {input_model.voice_id}")
        
        # Start a session with the assistant
        client.start(assistant=assistant)
        
        # Send the text
        logger.info(f"Sending text: {input_model.text}")
        client.send_text(input_model.text)
        
        # Wait for completion if requested
        if input_model.wait_for_completion:
            logger.info(f"Waiting for completion ({input_model.wait_time} seconds)...")
            time.sleep(input_model.wait_time)
        
        # Stop the client
        client.stop()
        
        return SayOutput(
            success=True,
            message="Successfully converted text to speech",
            audio_url="audio_url_would_be_here_in_full_implementation"  # In a real implementation, we'd return the actual URL
        ).dict()
        
    except ImportError as e:
        logger.error(f"Failed to import required module: {e}")
        return SayOutput(
            success=False,
            message=f"Error: Failed to import required module: {e}",
            audio_url=None
        ).dict()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return SayOutput(
            success=False,
            message=f"Error: {str(e)}",
            audio_url=None
        ).dict() 