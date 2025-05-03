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
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Add the src directory to the Python path to enable relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
# Reduce noise from MCP library
logging.getLogger("mcp").setLevel(logging.ERROR)

# Load MCP configuration
CONFIG_PATH = os.path.join(os.path.dirname(current_dir), "common", "mcp_config.yaml")

async def open_mcp_session(server_conf: dict) -> ClientSession:
    """
    Open and initialize an MCP client session.
    
    Args:
        server_conf: The server configuration from mcp_config.yaml
        
    Returns:
        An initialized MCP ClientSession
    """
    # Process environment variables in the config
    env = {}
    for key, value in server_conf.get("env", {}).items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            env[key] = os.environ.get(env_var, "")
        else:
            env[key] = value
    
    logger.warning(f"Starting server with command: {server_conf['command']} {' '.join(server_conf.get('args', []))}")
    
    # Create server parameters
    params = StdioServerParameters(
        command=server_conf["command"],
        args=server_conf.get("args", []),
        env=env,
    )
    
    # Create and initialize the client session
    read_stream, write_stream = await stdio_client(params).__aenter__()
    session = await ClientSession(read_stream, write_stream).__aenter__()
    await session.initialize()
    
    return session

async def init_mcp_client(agent_name: str) -> ClientSession:
    """
    Initialize and return an MCP ClientSession for the given agent_name using mcp_config.yaml.
    
    Args:
        agent_name (str): The name of the agent to initialize (e.g., "vapi-agent")
        
    Returns:
        ClientSession: An initialized MCP client session for the specified agent
    """
    try:
        # Load MCP server configurations
        import yaml
        with open(CONFIG_PATH) as f:
            config = yaml.safe_load(f)
            
        server_conf = config.get("mcpServers", {}).get(agent_name)
        if not server_conf:
            raise KeyError(f"No MCP server configuration found for agent '{agent_name}'")
            
        # Create and return the MCP session
        return await open_mcp_session(server_conf)
        
    except FileNotFoundError:
        logger.error(f"Config file not found: {CONFIG_PATH}")
        raise
    except Exception as e:
        logger.error(f"Error initializing MCP client: {e}")
        raise

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

async def main_async():
    """Main entry point for the chat bridge."""
    args = parse_args()
    
    logger.info("Starting chat bridge")
    
    try:
        # Initialize MCP clients
        logger.warning("Initializing Vapi agent...")
        vapi_session = await init_mcp_client("vapi-agent")
        logger.warning("Vapi agent initialized successfully!")
        
        logger.warning("Initializing Arcade agent...")
        arcade_session = await init_mcp_client("arcade-agent")
        logger.warning("Arcade agent initialized successfully!")
        
        logger.info("Successfully initialized MCP client sessions")
        
        # Check available voices
        voices_result = await vapi_session.call_tool("list_voices_tool", {})
        if not voices_result:
            logger.warning("Failed to list voices: Unknown error")
        else:
            voices_data = json.loads(str(voices_result.content[0].text))
            if voices_data.get("voices"):
                voice_ids = [v.get("voice_id") for v in voices_data.get("voices", [])]
                logger.info(f"Available voices: {', '.join(voice_ids)}")
        
        # Welcome message
        welcome_message = "Welcome to your voice-controlled calendar assistant. You can say things like 'Schedule a meeting tomorrow at 2 PM'."
        say_result = await vapi_session.call_tool("say_tool", {
            "text": welcome_message,
            "voice_id": args.voice
        })
        
        if not say_result:
            logger.error("Failed to say welcome message")
            return
        
        # Main interaction loop
        while True:
            # Listen for user input
            logger.info("Listening for user input...")
            
            if args.test_mode:
                # Simulate input in test mode
                logger.info("TEST MODE: Simulating user input")
                listen_text = "Schedule a language learning study session tomorrow at 3 PM"
            else:
                # Real listening
                listen_result = await vapi_session.call_tool("listen_tool", {
                    "max_listen_time": 30
                })
                
                if not listen_result:
                    error_message = "Failed to listen: Unknown error"
                    logger.error(error_message)
                    await vapi_session.call_tool("say_tool", {
                        "text": "Sorry, I couldn't hear you. Please try again.",
                        "voice_id": args.voice
                    })
                    continue
                
                # Parse the result text from the response
                result_data = json.loads(str(listen_result.content[0].text))
                listen_text = result_data.get("text", "")
            
            # Process the user input
            logger.info(f"User said: {listen_text}")
            
            # Check if user wants to exit
            if any(word in listen_text.lower() for word in ["exit", "quit", "stop", "goodbye", "bye"]):
                await vapi_session.call_tool("say_tool", {
                    "text": "Goodbye! Have a great day.",
                    "voice_id": args.voice
                })
                break
            
            # Check if the input is about scheduling
            if any(word in listen_text.lower() for word in ["schedule", "create", "add", "set up", "appointment", "meeting", "event"]):
                # Extract event details
                event_details = extract_event_details(listen_text)
                
                # Confirm with the user
                confirmation_text = f"I'll schedule a {event_details['summary']} from {event_details['start_datetime']} to {event_details['end_datetime']}. Is that correct?"
                
                await vapi_session.call_tool("say_tool", {
                    "text": confirmation_text,
                    "voice_id": args.voice
                })
                
                # In a real implementation, we would listen for confirmation
                # For this example, we'll assume the user confirms
                
                # Create the event
                logger.info(f"Creating event with details: {event_details}")
                event_result = await arcade_session.call_tool("create_event_tool", event_details)
                
                if not event_result:
                    error_message = "Failed to create event: Unknown error"
                    logger.error(error_message)
                    await vapi_session.call_tool("say_tool", {
                        "text": f"Sorry, I couldn't create the event. {error_message}",
                        "voice_id": args.voice
                    })
                else:
                    result_data = json.loads(str(event_result.content[0].text))
                    event_id = result_data.get("event_id", "unknown ID")
                    
                    success_message = f"Great! I've scheduled your {event_details['summary']}."
                    logger.info(f"Event created successfully: {event_id}")
                    await vapi_session.call_tool("say_tool", {
                        "text": success_message,
                        "voice_id": args.voice
                    })
                
                # Exit after one successful interaction in test mode
                if args.test_mode:
                    logger.info("TEST MODE: Exiting after one interaction")
                    break
            else:
                # Handle other types of input
                await vapi_session.call_tool("say_tool", {
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
    asyncio.run(main_async()) 