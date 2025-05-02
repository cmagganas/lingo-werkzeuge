"""
MCP server for Vapi agent, providing text-to-speech and speech-to-text capabilities.
"""
import os
import asyncio
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

# Import the tool implementations
from .tools.say import say
from .tools.listen import listen
from .tools.list_voices import list_voices

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
SAY_TOOL = Tool(
    name="say",
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
)

LISTEN_TOOL = Tool(
    name="listen",
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
)

LIST_VOICES_TOOL = Tool(
    name="list_voices",
    description="List available Rime AI voices for use with Vapi",
    inputSchema={
        "type": "object",
        "properties": {}
    }
)

async def serve() -> None:
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
        return [SAY_TOOL, LISTEN_TOOL, LIST_VOICES_TOOL]
    
    @server.call_tool("say")
    async def call_say(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle calls to the 'say' tool."""
        logger.info(f"Received call to 'say' tool with parameters: {parameters}")
        return say(parameters)
    
    @server.call_tool("listen")
    async def call_listen(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle calls to the 'listen' tool."""
        logger.info(f"Received call to 'listen' tool with parameters: {parameters}")
        return listen(parameters)
    
    @server.call_tool("list_voices")
    async def call_list_voices(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle calls to the 'list_voices' tool."""
        logger.info(f"Received call to 'list_voices' tool with parameters: {parameters}")
        return list_voices(parameters)
    
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
    asyncio.run(serve()) 