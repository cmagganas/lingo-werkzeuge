#!/usr/bin/env python3
"""
MCP server for Vapi agent, providing text-to-speech and speech-to-text capabilities.
"""
import os
import sys
import asyncio
import logging
from typing import Dict, Any, Optional, List, Sequence
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Add the src directory to the Python path to enable relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, src_dir)

# Import the tool implementations
from src.agents.vapi_agent.tools.say import say
from src.agents.vapi_agent.tools.listen import listen
from src.agents.vapi_agent.tools.list_voices import list_voices

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Define MCP tools
TOOLS = [
    Tool(
        name="say_tool",
        description="Convert text to speech using Vapi with Rime AI voices",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to convert to speech"
                },
                "voice_id": {
                    "type": "string",
                    "description": "The Rime AI voice ID to use (default: samantha)"
                },
                "wait_for_completion": {
                    "type": "boolean",
                    "description": "Whether to wait for the speech to complete (default: true)"
                },
                "wait_time": {
                    "type": "integer",
                    "description": "Time to wait for response in seconds if wait_for_completion is true (default: 10)"
                }
            },
            "required": ["text"]
        }
    ),
    Tool(
        name="listen_tool",
        description="Listen for speech and convert to text using Vapi",
        inputSchema={
            "type": "object",
            "properties": {
                "max_listen_time": {
                    "type": "integer",
                    "description": "Maximum time to listen in seconds (default: 30)"
                },
                "language": {
                    "type": "string",
                    "description": "Language code for speech recognition (default: en-US)"
                }
            }
        }
    ),
    Tool(
        name="list_voices_tool",
        description="List available Rime AI voices for use with Vapi",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
]

async def main():
    """Start the MCP server for the Vapi agent."""
    logger.info("Starting Vapi Agent MCP Server")
    
    # Check for API key
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        logger.warning("VAPI_API_KEY environment variable not set. Some features may be limited.")
    
    # Create the MCP server
    server = Server("vapi-agent")
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """Register all available tools with the MCP server."""
        return TOOLS
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Handle calls to tools.
        
        Args:
            name: The name of the tool to call
            arguments: The arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        logger.info(f"Received call to '{name}' with arguments: {arguments}")
        
        result = None
        if name == "say_tool":
            result = say(arguments)
        elif name == "listen_tool":
            result = listen(arguments)
        elif name == "list_voices_tool":
            result = list_voices(arguments)
        else:
            logger.error(f"Unknown tool: {name}")
            return [TextContent(f"Error: Unknown tool '{name}'")]
        
        # Convert the result to a text content
        return [TextContent(str(result))]
    
    # Initialize and run the server
    try:
        options = server.create_initialization_options()
        logger.info("Initializing stdio server connection...")
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Server running. Waiting for requests...")
            await server.run(read_stream, write_stream, options)
    except Exception as e:
        logger.exception(f"Critical Error: Server stopped due to unhandled exception: {e}")
        raise
    finally:
        logger.info("Vapi Agent MCP Server shutting down.")

if __name__ == "__main__":
    # Run the server
    asyncio.run(main()) 