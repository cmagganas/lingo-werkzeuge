#!/usr/bin/env python3
"""
Bridge for connecting the Vapi agent (speech) and Arcade agent (Google Calendar).
Allows for voice-based interaction with calendar functions.
"""

import os
import sys
import re
import json
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Import utility functions
# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.utils import init_mcp_client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def extract_event_details(text: str) -> Dict[str, Any]:
    """
    Extract event details from a text string.
    
    Args:
        text: The text to extract event details from
        
    Returns:
        Dictionary containing the extracted event details
    """
    # This is a simplified version that would be improved with NLP
    # In a real implementation, this would use more sophisticated techniques
    
    # Default values
    event = {
        "summary": "Meeting",
        "start_datetime": (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S"),
        "end_datetime": (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"),
    }
    
    # Extract summary
    summary_match = re.search(r"(?:schedule|create|add|set up)(?: a| an)? ([\w\s]+)(?:meeting|call|event|appointment)?", text, re.IGNORECASE)
    if summary_match:
        event["summary"] = summary_match.group(1).strip()
    
    # In a real implementation, we would also extract date, time, duration, etc.
    # This is just a simplified example
    
    return event

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Chat bridge for Vapi and Arcade agents")
    parser.add_argument("--voice", type=str, default="samantha", help="Rime AI voice to use")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode with simulated input")
    return parser.parse_args()

def main():
    """Main entry point for the chat bridge."""
    args = parse_args()
    
    logger.info("Starting chat bridge")
    
    try:
        # Initialize MCP clients
        vapi_client = init_mcp_client("vapi-agent")
        arcade_client = init_mcp_client("arcade-agent")
        
        logger.info("Successfully initialized MCP clients")
        
        # Check available voices
        voices_result = vapi_client.execute("list_voices", {})
        if not voices_result.get("success", False):
            logger.warning(f"Failed to list voices: {voices_result.get('message', 'Unknown error')}")
        else:
            logger.info(f"Available voices: {', '.join([v['voice_id'] for v in voices_result.get('voices', [])])}")
        
        # Welcome message
        welcome_message = "Welcome to your voice-controlled calendar assistant. You can say things like 'Schedule a meeting tomorrow at 2 PM'."
        say_result = vapi_client.execute("say", {
            "text": welcome_message,
            "voice_id": args.voice
        })
        
        if not say_result.get("success", False):
            logger.error(f"Failed to say welcome message: {say_result.get('message', 'Unknown error')}")
            return
        
        # Main interaction loop
        while True:
            # Listen for user input
            logger.info("Listening for user input...")
            
            if args.test_mode:
                # Simulate input in test mode
                logger.info("TEST MODE: Simulating user input")
                listen_result = {
                    "success": True,
                    "text": "Schedule a language learning study session tomorrow at 3 PM"
                }
            else:
                # Real listening
                listen_result = vapi_client.execute("listen", {
                    "max_listen_time": 30
                })
            
            if not listen_result.get("success", False):
                error_message = f"Failed to listen: {listen_result.get('message', 'Unknown error')}"
                logger.error(error_message)
                vapi_client.execute("say", {
                    "text": "Sorry, I couldn't hear you. Please try again.",
                    "voice_id": args.voice
                })
                continue
            
            # Process the user input
            user_text = listen_result.get("text", "")
            logger.info(f"User said: {user_text}")
            
            # Check if user wants to exit
            if any(word in user_text.lower() for word in ["exit", "quit", "stop", "goodbye", "bye"]):
                vapi_client.execute("say", {
                    "text": "Goodbye! Have a great day.",
                    "voice_id": args.voice
                })
                break
            
            # Check if the input is about scheduling
            if any(word in user_text.lower() for word in ["schedule", "create", "add", "set up", "appointment", "meeting", "event"]):
                # Extract event details
                event_details = extract_event_details(user_text)
                
                # Confirm with the user
                confirmation_text = f"I'll schedule a {event_details['summary']} from {event_details['start_datetime']} to {event_details['end_datetime']}. Is that correct?"
                
                vapi_client.execute("say", {
                    "text": confirmation_text,
                    "voice_id": args.voice
                })
                
                # In a real implementation, we would listen for confirmation
                # For this example, we'll assume the user confirms
                
                # Create the event
                logger.info(f"Creating event with details: {event_details}")
                event_result = arcade_client.execute("create_event", event_details)
                
                if not event_result.get("success", False):
                    error_message = f"Failed to create event: {event_result.get('message', 'Unknown error')}"
                    logger.error(error_message)
                    vapi_client.execute("say", {
                        "text": f"Sorry, I couldn't create the event. {error_message}",
                        "voice_id": args.voice
                    })
                else:
                    success_message = f"Great! I've scheduled your {event_details['summary']}."
                    logger.info(f"Event created successfully: {event_result.get('event_id', 'unknown ID')}")
                    vapi_client.execute("say", {
                        "text": success_message,
                        "voice_id": args.voice
                    })
                
                # Exit after one successful interaction in test mode
                if args.test_mode:
                    logger.info("TEST MODE: Exiting after one interaction")
                    break
            else:
                # Handle other types of input
                vapi_client.execute("say", {
                    "text": "I'm not sure how to help with that. I can schedule events for you. Try saying 'Schedule a meeting tomorrow at 2 PM'.",
                    "voice_id": args.voice
                })
    
    except KeyboardInterrupt:
        logger.info("User interrupted the program")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        logger.info("Chat bridge shutting down")

if __name__ == "__main__":
    main() 