import logging
import sys
import threading
import time
from typing import Optional

from lingo_werkzeuge.convolingo.api.client import VapiClient
from lingo_werkzeuge.convolingo.utils.config import (
    config, DEFAULT_TARGET_LANGUAGE, DEFAULT_ORIGIN_LANGUAGE, DEFAULT_CHAPTER
)
from lingo_werkzeuge.convolingo.utils.logging_setup import setup_logging

# Set up logging
logger = setup_logging(__name__, log_level=config.log_level, log_dir=config.log_dir)

def start_interactive_session(
    target_language: str = DEFAULT_TARGET_LANGUAGE,
    native_language: str = DEFAULT_ORIGIN_LANGUAGE,
    chapter: str = DEFAULT_CHAPTER,
    user_id: Optional[str] = None
) -> None:
    """
    Start an interactive ConvoLingo session
    
    Args:
        target_language: The language to learn
        native_language: The user's native language
        chapter: The current chapter or module being studied
        user_id: Optional user ID for personalization
    """
    logger.info(f"Starting interactive session for {target_language}")
    
    # Check for API key
    if not config.api_key:
        print("Error: VAPI API key not found. Please set it in your environment.")
        print("You can create one at https://vapi.ai and set it with:")
        print("export VAPI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Initialize VAPI client
    client = VapiClient()
    
    # Welcome message
    print("\n===============================================")
    print(f"  Welcome to ConvoLingo - {target_language} Learning!")
    print("===============================================\n")
    print(f"You'll be learning {target_language} through conversation.")
    print("Type your messages and press Enter to send.")
    print("Type 'exit' or 'quit' to end the session.\n")
    print("Connecting to language assistant...")
    
    # Connect to VAPI
    if not client.connect(
        target_language=target_language,
        native_language=native_language,
        chapter=chapter,
        user_id=user_id
    ):
        print("Error: Failed to connect to VAPI. Please check your API key and internet connection.")
        sys.exit(1)
    
    print("\nConnected! You can start chatting with your language assistant now.\n")
    
    # Set up a flag for the connection loop
    should_continue = threading.Event()
    should_continue.set()  # Start with True
    
    # Start connection maintenance in a separate thread
    maintenance_thread = threading.Thread(
        target=client.maintain_connection,
        args=(lambda: should_continue.is_set(),)
    )
    maintenance_thread.daemon = True
    maintenance_thread.start()
    
    # Main interaction loop
    try:
        while True:
            # Get user input
            user_input = input("> ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                print("\nEnding your language learning session...")
                should_continue.clear()  # Signal the maintenance thread to stop
                break
            
            # Send message to assistant
            if not client.send_message(user_input):
                print("Error: Failed to send message. The connection may have been lost.")
                should_continue.clear()
                break
    
    except KeyboardInterrupt:
        print("\nEnding your language learning session...")
        should_continue.clear()
    
    # Wait for maintenance thread to finish
    maintenance_thread.join(timeout=2.0)
    
    print("\nThank you for using ConvoLingo! Keep practicing!")

if __name__ == "__main__":
    # This can be run directly for testing
    start_interactive_session() 