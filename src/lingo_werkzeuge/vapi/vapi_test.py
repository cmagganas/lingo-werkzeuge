#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("VAPI_API_KEY")
if not api_key:
    print("Error: VAPI_API_KEY environment variable not set.")
    print("Please set your API key in the .env file or environment.")
    sys.exit(1)

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
            "voiceId": "samantha",  # Rime AI voice
        },
        "transcriber": {
            "model": "nova-3",
            "language": "en-US",
            "provider": "deepgram"
        }
    }
    
    print("\nAttempting to create a test assistant...")
    print("Assistant configuration:", assistant)
    
    # Try to use the client
    try:
        # Start a session with the assistant
        client.start(assistant=assistant)
        print("\nSuccess! Assistant created successfully with Rime AI voice.")
        print("You can now try sending a message to test it.")
        
        # Send a test message
        message = "Hello, how are you today?"
        print(f"\nSending test message: '{message}'")
        
        # Use send_text instead of message (the correct method)
        client.send_text(message)
        
        # Wait a bit and stop the client
        import time
        print("Waiting for response...")
        time.sleep(10)  # Let the system process longer
        
        client.stop()
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nError using Vapi client: {e}")
        
except ImportError as e:
    print(f"Error: Failed to import required module: {e}")
    print("Please make sure you have installed vapi_python correctly.")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1) 