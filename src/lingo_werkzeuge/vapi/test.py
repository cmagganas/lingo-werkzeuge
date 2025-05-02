#!/usr/bin/env python3
"""
Test module for Vapi integration with Rime AI voices.
"""
import os
import sys
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

def test_assistant(
    voice_id: str = "samantha",
    test_message: str = "Hello, how are you today?",
    wait_time: int = 10
) -> bool:
    """
    Test the Vapi assistant with Rime AI voice.
    
    Args:
        voice_id: The Rime AI voice ID to use
        test_message: Message to send to the assistant
        wait_time: Time to wait for response in seconds
        
    Returns:
        bool: True if test was successful, False otherwise
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        print("Error: VAPI_API_KEY environment variable not set.")
        print("Please set your API key in the .env file or environment.")
        return False
    
    try:
        # Import the Vapi client
        from vapi_python import Vapi
        
        print("Successfully imported vapi_python module.")
        
        # Initialize the Vapi client
        client = Vapi(api_key=api_key)
        print("Successfully initialized Vapi client.")
        
        # Create assistant configuration with Rime AI voice
        assistant = {
            "model": {
                "model": "gpt-3.5-turbo", 
                "provider": "openai",
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant named Emma."
                    }
                ]
            },
            "voice": {
                "provider": "rime-ai",
                "voiceId": voice_id,  # Rime AI voice
            },
            "transcriber": {
                "model": "nova-3",
                "language": "en-US",
                "provider": "deepgram"
            }
        }
        
        print(f"\nAttempting to create a test assistant with voice: {voice_id}...")
        print("Assistant configuration:", assistant)
        
        # Try to use the client
        try:
            # Start a session with the assistant
            client.start(assistant=assistant)
            print("\nSuccess! Assistant created successfully with Rime AI voice.")
            print("You can now try sending a message to test it.")
            
            # Send a test message
            print(f"\nSending test message: '{test_message}'")
            
            # Use send_text instead of message (the correct method)
            client.send_text(test_message)
            
            # Wait a bit and stop the client
            print(f"Waiting for response (up to {wait_time} seconds)...")
            time.sleep(wait_time)  # Let the system process
            
            client.stop()
            print("\nTest completed successfully!")
            return True
            
        except Exception as e:
            print(f"\nError using Vapi client: {e}")
            return False
            
    except ImportError as e:
        print(f"Error: Failed to import required module: {e}")
        print("Please make sure you have installed vapi_python correctly.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def list_rime_voices() -> Dict[str, str]:
    """
    List available Rime AI voices with descriptions.
    
    Returns:
        Dict[str, str]: Dictionary of voice IDs and descriptions
    """
    voices = {
        "samantha": "Female, clear and professional",
        "elena": "Female, warm and friendly",
        "nicholas": "Male, authoritative and clear",
        "tyler": "Male, conversational and friendly",
        "maya": "Female, younger sounding voice",
        "ally": "Female, energetic and upbeat"
    }
    
    print("Available Rime AI Voices:")
    for voice_id, description in voices.items():
        print(f"- {voice_id}: {description}")
        
    return voices

if __name__ == "__main__":
    """Run the test when script is executed directly"""
    print("Vapi Assistant Test with Rime AI Voice")
    print("=====================================")
    
    # Show available voices
    voices = list_rime_voices()
    print()
    
    # Ask for voice selection
    default_voice = "samantha"
    voice_choice = input(f"Choose a voice (default: {default_voice}): ").strip() or default_voice
    
    # Run the test
    success = test_assistant(voice_id=voice_choice)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 