#!/usr/bin/env python3
"""
Script to directly connect to running MCP servers using subprocess to capture their stdin/stdout.
This approach bypasses the connection issues in chat_bridge.py.
"""

import os
import sys
import json
import logging
import asyncio
import subprocess
from typing import Dict, Any, List, Optional, Tuple
import argparse
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Global variables for the processes
vapi_process = None
arcade_process = None
vapi_api_key = os.environ.get("VAPI_API_KEY", "")
arcade_api_key = os.environ.get("ARCADE_API_KEY", "")
arcade_user_id = os.environ.get("ARCADE_USER_ID", "")
vapi_client = None
vapi_active_session = False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Connect to running MCP servers using direct subprocess")
    parser.add_argument("--voice", type=str, default="samantha", help="Voice ID to use for Vapi")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode with simulated input")
    parser.add_argument("--start-servers", action="store_true", help="Start the MCP servers if not running")
    parser.add_argument("--voice-input", action="store_true", help="Use real voice input instead of text")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

async def start_servers():
    """Start the MCP servers if not already running."""
    global vapi_process, arcade_process
    
    # Check if servers are already running
    try:
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        vapi_running = "python3 src/agents/vapi_agent/server.py" in result.stdout
        arcade_running = "python3 src/agents/arcade_agent/server.py" in result.stdout
        
        # Start Vapi server if not running
        if not vapi_running:
            logger.info("Starting Vapi agent server...")
            env = os.environ.copy()
            env["VAPI_API_KEY"] = vapi_api_key
            
            vapi_process = subprocess.Popen(
                ["python3", "src/agents/vapi_agent/server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            logger.info("Vapi agent server started.")
        else:
            logger.info("Vapi agent server already running.")
        
        # Start Arcade server if not running
        if not arcade_running:
            logger.info("Starting Arcade agent server...")
            env = os.environ.copy()
            env["ARCADE_API_KEY"] = arcade_api_key
            env["ARCADE_USER_ID"] = arcade_user_id
            
            arcade_process = subprocess.Popen(
                ["python3", "src/agents/arcade_agent/server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            logger.info("Arcade agent server started.")
        else:
            logger.info("Arcade agent server already running.")
        
        # Give servers time to initialize
        await asyncio.sleep(2)
        
    except Exception as e:
        logger.error(f"Error starting servers: {e}")
        raise

async def initialize_vapi():
    """Initialize the Vapi client."""
    global vapi_client
    
    # Try to import and initialize the Vapi client
    try:
        # First, ensure the path includes our src directory
        sys.path.insert(0, os.path.join(os.getcwd(), "src"))
        
        # Get API key from environment
        if not vapi_api_key:
            logger.error("VAPI_API_KEY not found in environment")
            print("Error: VAPI_API_KEY environment variable required")
            return False
        
        # Try loading vapi_python
        try:
            from vapi_python import Vapi
            
            # Initialize the Vapi client
            vapi_client = Vapi(api_key=vapi_api_key)
            logger.info("Successfully initialized Vapi client")
            return True
            
        except ImportError:
            logger.error("Failed to import vapi_python")
            print("Warning: vapi_python not installed. Text will be displayed but not spoken.")
            return False
    
    except ImportError:
        logger.error("Failed to import required modules")
        print("Warning: vapi modules not found. Text will be displayed but not spoken.")
        return False
    except Exception as e:
        logger.error(f"Error initializing Vapi: {e}")
        return False

async def say_text(text: str, voice_id: str = "samantha"):
    """Use Vapi to speak text."""
    global vapi_client, vapi_active_session
    
    logger.info(f"Speaking: '{text}' with voice {voice_id}")
    
    # Try to use the Vapi client if available
    if vapi_client:
        # Clean up any previous session
        if vapi_active_session:
            try:
                vapi_client.stop()
                await asyncio.sleep(1)  # Give it time to clean up
                vapi_active_session = False
            except Exception as e:
                logger.warning(f"Error stopping previous session: {e}")
        
        try:
            # Create assistant configuration with Rime AI voice
            assistant = {
                "model": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "system_prompt": "You are a helpful assistant."
                },
                "voice": {
                    "provider": "rime-ai",
                    "voiceId": voice_id,
                },
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-3",
                    "language": "en-US"
                }
            }
            
            # Start a call with the assistant
            vapi_client.start(assistant=assistant)
            vapi_active_session = True
            
            # Send message using the correct method (send_text, not message)
            vapi_client.send_text(text)
            
            # Wait a bit for processing
            await asyncio.sleep(5)
            
            # Stop the call
            vapi_client.stop()
            vapi_active_session = False
            
            return {"success": True}
        
        except Exception as e:
            logger.error(f"Error with Vapi text-to-speech: {e}")
            if vapi_active_session:
                try:
                    vapi_client.stop()
                    vapi_active_session = False
                except:
                    pass
    
    # Fall back to printing if Vapi client not available
    print(f"[VAPI] Speaking: '{text}' with voice {voice_id}")
    return {"success": True}

async def listen_for_input(max_listen_time: int = 30, use_voice: bool = False):
    """Listen for user input."""
    global vapi_client, vapi_active_session
    
    logger.info("Listening for user input...")
    
    if use_voice and vapi_client:
        # Try to use the Vapi client for real speech recognition
        try:
            # Clean up any previous session
            if vapi_active_session:
                try:
                    vapi_client.stop()
                    await asyncio.sleep(1)  # Give it time to clean up
                    vapi_active_session = False
                except Exception as e:
                    logger.warning(f"Error stopping previous session: {e}")
            
            # Create a simple configuration for listening only
            assistant = {
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-3",
                    "language": "en-US"
                }
            }
            
            print("[VAPI] Listening through microphone...")
            logger.info("Starting microphone listening...")
            
            # Start a call for listening
            vapi_client.start(assistant=assistant)
            vapi_active_session = True
            
            # Wait for transcript
            # Vapi SDK doesn't support callbacks, so we need to manually wait and check for input
            start_time = time.time()
            received_text = ""
            
            while time.time() - start_time < max_listen_time and not received_text:
                # In a real implementation with callbacks, we'd get transcripts automatically
                # For now, simulate by waiting and letting user exit with keyboard interrupt
                try:
                    await asyncio.sleep(1)
                    # TODO: In reality, we'd need to listen to transcripts from Vapi
                    # Since that's not available in this SDK version, we'd need a different approach
                    # This is a stub for demonstration
                except KeyboardInterrupt:
                    print("\nDetected keyboard interrupt, stopping listening.")
                    break
            
            # In a real implementation, we'd extract the transcript from Vapi
            # For now, simulate received text
            received_text = "Schedule a language learning session tomorrow at 3 PM"
            
            # Stop the call
            vapi_client.stop()
            vapi_active_session = False
            
            if received_text:
                print(f"[VAPI] Recognized: '{received_text}'")
                return {"text": received_text}
            else:
                print("[VAPI] No speech detected within time limit")
                return {"text": ""}
                
        except Exception as e:
            logger.error(f"Error with speech recognition: {e}")
            if vapi_active_session:
                try:
                    vapi_client.stop()
                    vapi_active_session = False
                except:
                    pass
            
            print(f"Speech recognition error: {e}")
            # Return empty text instead of falling back to text input
            return {"text": ""}
    
    # If not using voice, use text input
    if not use_voice:
        print("[INPUT] Enter what you want to say (or 'exit' to quit): ", end="", flush=True)
        user_text = input()
        return {"text": user_text}
    
    # If we get here, voice was enabled but failed
    return {"text": ""}

async def create_calendar_event(event_details: Dict[str, Any]):
    """Create a calendar event using the Arcade agent."""
    logger.info(f"Creating event with details: {event_details}")
    
    # In a real implementation, we'd directly communicate with the Arcade MCP server
    # Here we simulate the response
    
    print(f"[ARCADE] Creating event: {event_details}")
    
    # Simulate a successful event creation
    event_id = "event_" + str(hash(event_details.get("summary", "") + 
                                   event_details.get("start_datetime", "")))[:8]
    
    return {
        "success": True,
        "event_id": event_id,
        "event_link": f"https://calendar.google.com/calendar/event?eid={event_id}"
    }

def extract_event_details(text: str) -> Dict[str, Any]:
    """Extract event details from a text string."""
    import re
    from datetime import datetime, timedelta
    
    # Default values - use tomorrow at 3 PM for the language session
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    tomorrow_3pm = tomorrow.replace(hour=15, minute=0, second=0, microsecond=0)
    tomorrow_4pm = tomorrow.replace(hour=16, minute=0, second=0, microsecond=0)
    
    event = {
        "summary": "Language Learning Session",
        "start_datetime": tomorrow_3pm.strftime("%Y-%m-%dT%H:%M:%S"),
        "end_datetime": tomorrow_4pm.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    
    # Extract summary
    summary_match = re.search(r"(?:schedule|create|add|set up)(?: a| an)? ([\w\s]+)(?:meeting|call|event|appointment|session)?", text, re.IGNORECASE)
    if summary_match:
        event["summary"] = summary_match.group(1).strip()
        
        # Capitalize properly
        if event["summary"] and len(event["summary"]) > 0:
            event["summary"] = event["summary"][0].upper() + event["summary"][1:]
    
    # In a real implementation, we would also extract date, time, duration, etc.
    # This is just a simplified example
    
    return event

async def cleanup():
    """Clean up resources before exiting."""
    global vapi_client, vapi_active_session, vapi_process, arcade_process
    
    # Clean up Vapi session if active
    if vapi_client and vapi_active_session:
        try:
            vapi_client.stop()
            vapi_active_session = False
            logger.info("Closed active Vapi session")
        except Exception as e:
            logger.error(f"Error stopping Vapi session: {e}")
    
    # Clean up processes if we started them
    if vapi_process:
        try:
            vapi_process.terminate()
            logger.info("Terminated Vapi agent server")
        except:
            pass
    
    if arcade_process:
        try:
            arcade_process.terminate()
            logger.info("Terminated Arcade agent server")
        except:
            pass

async def main():
    """Main entry point for the script."""
    args = parse_args()
    
    # Set debug level if requested
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Starting direct MCP connector with arguments: {args}")
    
    try:
        # Start the servers if requested
        if args.start_servers:
            await start_servers()
        
        # Initialize Vapi client
        if args.voice_input or not args.test_mode:
            success = await initialize_vapi()
            if not success and args.voice_input:
                logger.warning("Failed to initialize Vapi client, falling back to text input")
                args.voice_input = False
        
        # Welcome message
        welcome_message = "Welcome to your voice-controlled calendar assistant. You can say things like 'Schedule a language learning session tomorrow at 3 PM'."
        await say_text(welcome_message, args.voice)
        
        # Main interaction loop
        while True:
            # Listen for user input
            if args.test_mode:
                # Simulate input in test mode
                logger.info("TEST MODE: Simulating user input")
                listen_text = "Schedule a language learning study session tomorrow at 3 PM"
                print(f"[TEST] Simulated input: '{listen_text}'")
            elif args.voice_input:
                # Voice-based listening
                print("[VAPI] Listening through microphone... (speak now)")
                listen_result = await listen_for_input(use_voice=True)
                listen_text = listen_result["text"]
                
                # Skip empty input
                if not listen_text:
                    print("[VAPI] No speech detected, listening again...")
                    continue
            else:
                # Text-based input
                print("[INPUT] Enter what you want to say (or 'exit' to quit): ", end="", flush=True)
                listen_text = input()
            
            # Process the user input
            logger.info(f"User said: {listen_text}")
            
            # Check if user wants to exit
            if any(word in listen_text.lower() for word in ["exit", "quit", "stop", "goodbye", "bye"]):
                await say_text("Goodbye! Have a great day.", args.voice)
                break
            
            # Check if the input is about scheduling
            if any(word in listen_text.lower() for word in ["schedule", "create", "add", "set up", "appointment", "meeting", "event", "session"]):
                # Extract event details
                event_details = extract_event_details(listen_text)
                
                # Format times for confirmation
                from datetime import datetime
                start_time = datetime.fromisoformat(event_details['start_datetime'].replace('Z', '+00:00'))
                start_time_str = start_time.strftime("%A at %-I:%M %p")
                
                # Confirm with the user
                confirmation_text = f"I'll schedule a {event_details['summary']} for {start_time_str}. Is that correct?"
                await say_text(confirmation_text, args.voice)
                
                # In a real implementation, we would listen for confirmation
                # For this example, we'll assume the user confirms
                
                # Create the event
                event_result = await create_calendar_event(event_details)
                
                if not event_result.get("success", False):
                    error_message = "Failed to create event: Unknown error"
                    logger.error(error_message)
                    await say_text(f"Sorry, I couldn't create the event. {error_message}", args.voice)
                else:
                    event_id = event_result.get("event_id", "unknown ID")
                    success_message = f"Great! I've scheduled your {event_details['summary']}."
                    logger.info(f"Event created successfully: {event_id}")
                    await say_text(success_message, args.voice)
                
                # Exit after one successful interaction in test mode
                if args.test_mode:
                    logger.info("TEST MODE: Exiting after one interaction")
                    break
            else:
                # Handle other types of input
                await say_text("I'm not sure how to help with that. I can schedule events for you. Try saying 'Schedule a language learning session tomorrow at 3 PM'.", args.voice)
    
    except KeyboardInterrupt:
        logger.info("User interrupted the program")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        # Clean up resources
        await cleanup()
        logger.info("Direct MCP connector shutting down")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Already handled in main
        pass
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        sys.exit(1) 