#!/usr/bin/env python3
"""
Simple demo script for the Lingo-Werkzeuge voice calendar assistant.
This script assumes the Vapi and Arcade servers are already running in separate terminals.
"""

import os
import logging
import asyncio
from subprocess import Popen, PIPE
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print a welcome banner for the demo."""
    print("""
    +-----------------------------------------------------------------+
    |                                                                 |
    |             LINGO-WERKZEUGE VOICE CALENDAR ASSISTANT            |
    |                                                                 |
    +-----------------------------------------------------------------+
    |                                                                 |
    |  This demo shows how the Vapi and Arcade agents work together.  |
    |  You can schedule calendar events using voice commands!         |
    |                                                                 |
    +-----------------------------------------------------------------+
    """)

async def demo_vapi_say(text, voice_id="samantha"):
    """Use the Vapi agent to say something."""
    print(f"[VAPI] Speaking: '{text}' with voice {voice_id}")
    
    # In a real implementation, we would use the MCP client to communicate with the Vapi server
    # For this demo, we'll simulate the response
    return {"success": True}

async def demo_vapi_listen():
    """Use the Vapi agent to listen for user input."""
    print("[VAPI] Listening for user input...")
    
    # Simulate the user saying something
    user_text = input("Enter what you want to say (or 'exit' to quit): ")
    
    # In a real implementation, we would use the MCP client to communicate with the Vapi server
    # For this demo, we'll just return the input text
    return {"text": user_text}

async def demo_arcade_create_event(summary, start_time, end_time):
    """Use the Arcade agent to create a calendar event."""
    event_details = {
        "summary": summary,
        "start_datetime": start_time,
        "end_datetime": end_time
    }
    
    print(f"[ARCADE] Creating event: {event_details}")
    
    # In a real implementation, we would use the MCP client to communicate with the Arcade server
    # For this demo, we'll simulate the response
    event_id = "event_" + str(hash(summary + start_time))[:8]
    return {"event_id": event_id, "success": True}

async def main():
    """Main demo function."""
    print_banner()
    
    # Welcome message
    await demo_vapi_say("Welcome to your voice-controlled calendar assistant. You can say things like 'Schedule a language learning session tomorrow at 3 PM'.")
    
    while True:
        # Listen for user input
        listen_result = await demo_vapi_listen()
        user_text = listen_result["text"]
        
        # Check if user wants to exit
        if user_text.lower() in ["exit", "quit", "goodbye", "bye"]:
            await demo_vapi_say("Goodbye! Have a great day.")
            break
        
        # Check if this is a calendar command
        if any(word in user_text.lower() for word in ["schedule", "create", "add", "set up", "appointment", "meeting", "event"]):
            # Extract event details (simplified)
            words = user_text.split()
            summary = " ".join(words[2:5]) if len(words) > 4 else "Meeting"
            
            # Use a simplified start and end time
            start_time = "2025-05-03T15:00:00"
            end_time = "2025-05-03T16:00:00"
            
            # Confirm with the user
            await demo_vapi_say(f"I'll schedule a {summary} tomorrow at 3 PM. Is that correct?")
            
            # Create the event
            event_result = await demo_arcade_create_event(summary, start_time, end_time)
            
            if event_result["success"]:
                await demo_vapi_say(f"Great! I've scheduled your {summary}.")
            else:
                await demo_vapi_say("Sorry, I couldn't create that event.")
        else:
            await demo_vapi_say("I'm not sure how to help with that. Try saying 'Schedule a language learning session tomorrow at 3 PM'.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")
    except Exception as e:
        logger.exception(f"Error in demo: {e}") 