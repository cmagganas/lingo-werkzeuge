#!/usr/bin/env python3
"""
Script to connect to running MCP servers and test functionality.
This assumes the Vapi and Arcade agent servers are already running in separate terminals.
"""

import os
import sys
import json
import logging
import argparse
import asyncio
from typing import Dict, Any, Optional
import subprocess

# Add the src directory to the Python path to enable relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, src_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Connect to running MCP servers and test functionality")
    parser.add_argument("--vapi-port", type=int, default=8080, help="Port for the Vapi agent server")
    parser.add_argument("--arcade-port", type=int, default=8081, help="Port for the Arcade agent server")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode with simulated responses")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

async def test_vapi_agent():
    """Test the Vapi agent with a simulated command."""
    print("Testing Vapi agent...")
    logger.info("Testing Vapi agent...")
    
    try:
        # Simulate sending a command to the server
        voice_id = "samantha"
        text = "Hello, this is a test message from the connector script."
        
        # In a real scenario, we would use sockets or other methods to communicate with the server
        # For now, we'll simulate a request/response
        
        # Simulate the response
        if args.test_mode:
            print(f"TEST MODE: Simulating saying text: '{text}' with voice: {voice_id}")
            logger.info(f"TEST MODE: Simulating saying text: '{text}' with voice: {voice_id}")
            return True
        else:
            # Try to use curl to call the Vapi service
            # This is a temporary solution - in a real implementation we would use proper MCP client
            cmd = ['curl', '-s', '-X', 'POST', f'http://localhost:{args.vapi_port}/say',
                   '-H', 'Content-Type: application/json',
                   '-d', f'{{"text": "{text}", "voice_id": "{voice_id}"}}']
            
            print(f"Running command: {' '.join(cmd)}")
            logger.info(f"Running command: {' '.join(cmd)}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                print(f"Response: {result.stdout}")
                logger.info(f"Response: {result.stdout}")
                return result.returncode == 0
            except subprocess.TimeoutExpired:
                print("Timeout waiting for Vapi agent response")
                logger.error("Timeout waiting for Vapi agent response")
                return False
            except Exception as e:
                print(f"Error calling Vapi agent: {e}")
                logger.error(f"Error calling Vapi agent: {e}")
                return False
    except Exception as e:
        print(f"Error testing Vapi agent: {e}")
        logger.error(f"Error testing Vapi agent: {e}")
        return False

async def test_arcade_agent():
    """Test the Arcade agent with a simulated event creation."""
    print("Testing Arcade agent...")
    logger.info("Testing Arcade agent...")
    
    try:
        # Simulate creating an event
        event_details = {
            "summary": "Test Meeting",
            "start_datetime": "2025-05-03T15:00:00",
            "end_datetime": "2025-05-03T16:00:00"
        }
        
        # In a real scenario, we would use MCP client to communicate with the server
        # For now, we'll simulate a request/response
        
        # Simulate the response
        if args.test_mode:
            print(f"TEST MODE: Simulating creating event: {event_details}")
            logger.info(f"TEST MODE: Simulating creating event: {event_details}")
            return True
        else:
            # Try to use curl to call the Arcade service
            # This is a temporary solution - in a real implementation we would use proper MCP client
            cmd = ['curl', '-s', '-X', 'POST', f'http://localhost:{args.arcade_port}/create-event',
                   '-H', 'Content-Type: application/json',
                   '-d', json.dumps(event_details)]
            
            print(f"Running command: {' '.join(cmd)}")
            logger.info(f"Running command: {' '.join(cmd)}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                print(f"Response: {result.stdout}")
                logger.info(f"Response: {result.stdout}")
                return result.returncode == 0
            except subprocess.TimeoutExpired:
                print("Timeout waiting for Arcade agent response")
                logger.error("Timeout waiting for Arcade agent response")
                return False
            except Exception as e:
                print(f"Error calling Arcade agent: {e}")
                logger.error(f"Error calling Arcade agent: {e}")
                return False
    except Exception as e:
        print(f"Error testing Arcade agent: {e}")
        logger.error(f"Error testing Arcade agent: {e}")
        return False

async def test_agents_connection():
    """Test connecting to and executing commands on both agents."""
    print("Starting agent connection tests...")
    logger.info("Starting agent connection tests...")
    
    # Test Vapi agent
    vapi_success = await test_vapi_agent()
    if vapi_success:
        print("Successfully tested Vapi agent")
        logger.info("Successfully tested Vapi agent")
    else:
        print("Failed to test Vapi agent")
        logger.error("Failed to test Vapi agent")
    
    # Test Arcade agent
    arcade_success = await test_arcade_agent()
    if arcade_success:
        print("Successfully tested Arcade agent")
        logger.info("Successfully tested Arcade agent")
    else:
        print("Failed to test Arcade agent")
        logger.error("Failed to test Arcade agent")
    
    # Report overall results
    if vapi_success and arcade_success:
        print("All agent tests passed successfully!")
        logger.info("All agent tests passed successfully!")
        return True
    else:
        print("Some agent tests failed.")
        logger.error("Some agent tests failed.")
        return False

async def main():
    """Main entry point of the script."""
    print("Starting agent connector script...")
    logger.info("Starting agent connector script...")
    
    # Test connecting to both agents
    success = await test_agents_connection()
    
    if success:
        print("Connection tests completed successfully.")
        logger.info("Connection tests completed successfully.")
        
        # In a real implementation, we would have additional functionality here
        # For now, we'll just exit with a success code
        return 0
    else:
        print("Connection tests failed. Please check that both agent servers are running.")
        logger.error("Connection tests failed. Please check that both agent servers are running.")
        return 1

if __name__ == "__main__":
    # Parse arguments
    args = parse_args()
    
    # Set log level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run the main function
    print(f"Starting with arguments: {args}")
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 