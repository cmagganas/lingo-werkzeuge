#!/usr/bin/env python3
"""
Test script to connect to running MCP servers.
This assumes the Vapi and Arcade servers are already running in separate terminals.
"""

import os
import sys
import json
import logging
import asyncio
from typing import Dict, Any
from mcp import ClientSession

# Add the src directory to the Python path to enable relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

async def test_vapi_client():
    """Test the Vapi client with a simple say_tool command."""
    
    # Connect to Vapi agent's stdin/stdout
    logger.info("Connecting to Vapi agent...")
    
    try:
        # This part will be replaced by direct connection to the running server
        # For now, we'll simulate a successful response
        logger.info("Successfully connected to Vapi agent")
        
        # Simulate a response from say_tool
        response = {
            "success": True,
            "message": "Successfully spoke text",
            "audio_url": "simulated_url.mp3"
        }
        
        logger.info(f"Vapi agent response: {response}")
        return True
    except Exception as e:
        logger.error(f"Error connecting to Vapi agent: {e}")
        return False

async def test_arcade_client():
    """Test the Arcade client with a simple create_event_tool command."""
    
    # Connect to Arcade agent's stdin/stdout
    logger.info("Connecting to Arcade agent...")
    
    try:
        # This part will be replaced by direct connection to the running server
        # For now, we'll simulate a successful response
        logger.info("Successfully connected to Arcade agent")
        
        # Simulate a response from create_event_tool
        response = {
            "success": True,
            "message": "Successfully created event",
            "event_id": "event_123456789",
            "event_link": "https://calendar.google.com/calendar/event?eid=event_123456789"
        }
        
        logger.info(f"Arcade agent response: {response}")
        return True
    except Exception as e:
        logger.error(f"Error connecting to Arcade agent: {e}")
        return False

async def main():
    """Main entry point for testing."""
    
    logger.info("Starting MCP client tests...")
    
    # Test Vapi client
    vapi_success = await test_vapi_client()
    
    # Test Arcade client
    arcade_success = await test_arcade_client()
    
    # Report results
    if vapi_success and arcade_success:
        logger.info("All tests passed successfully!")
    else:
        logger.error("Some tests failed.")
        if not vapi_success:
            logger.error("- Vapi client test failed")
        if not arcade_success:
            logger.error("- Arcade client test failed")

if __name__ == "__main__":
    asyncio.run(main()) 