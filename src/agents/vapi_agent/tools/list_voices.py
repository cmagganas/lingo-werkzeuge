"""
Tool for listing available Rime AI voices for use with Vapi.
"""
import logging
from typing import Dict, Any, List
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceDetails(BaseModel):
    """Details about a voice."""
    voice_id: str = Field(..., description="The voice ID to use with Vapi")
    description: str = Field(..., description="Description of the voice")
    gender: str = Field(..., description="Gender of the voice (male/female)")

class ListVoicesInput(BaseModel):
    """Input schema for the 'list_voices' tool."""
    # No input parameters required
    pass

class ListVoicesOutput(BaseModel):
    """Output schema for the 'list_voices' tool."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")
    voices: List[VoiceDetails] = Field(default_factory=list, description="List of available voices")

def list_voices(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    List available Rime AI voices for use with Vapi.
    
    Args:
        input_data: Dictionary containing the input parameters (empty for this tool)
        
    Returns:
        Dictionary containing the output parameters with voice details
    """
    # Parse input (empty for this tool)
    _ = ListVoicesInput(**input_data)
    
    try:
        # Define available voices
        voices = [
            VoiceDetails(
                voice_id="samantha",
                description="Clear and professional",
                gender="female"
            ),
            VoiceDetails(
                voice_id="elena",
                description="Warm and friendly",
                gender="female"
            ),
            VoiceDetails(
                voice_id="nicholas",
                description="Authoritative and clear",
                gender="male"
            ),
            VoiceDetails(
                voice_id="tyler",
                description="Conversational and friendly",
                gender="male"
            ),
            VoiceDetails(
                voice_id="maya",
                description="Younger sounding voice",
                gender="female"
            ),
            VoiceDetails(
                voice_id="ally",
                description="Energetic and upbeat",
                gender="female"
            )
        ]
        
        # Log the voices
        logger.info(f"Found {len(voices)} Rime AI voices")
        
        # Return the voices
        return ListVoicesOutput(
            success=True,
            message="Successfully retrieved available voices",
            voices=voices
        ).dict()
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ListVoicesOutput(
            success=False,
            message=f"Error: {str(e)}",
            voices=[]
        ).dict() 