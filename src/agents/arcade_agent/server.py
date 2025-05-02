"""
MCP server for Arcade agent, providing access to Google Workspace tools like Calendar.
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
from .tools.create_event import create_event

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
CREATE_EVENT_TOOL = Tool(
    name="create_event",
    description="Create a new event/meeting/sync/meetup in the specified calendar using Google Calendar",
    inputSchema={
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "The title of the event"
            },
            "start_datetime": {
                "type": "string",
                "description": "The datetime when the event starts in ISO 8601 format, e.g., '2024-12-31T15:30:00'"
            },
            "end_datetime": {
                "type": "string",
                "description": "The datetime when the event ends in ISO 8601 format, e.g., '2024-12-31T17:30:00'"
            },
            "calendar_id": {
                "type": "string",
                "description": "The ID of the calendar to create the event in, usually 'primary'"
            },
            "description": {
                "type": "string",
                "description": "The description of the event"
            },
            "location": {
                "type": "string",
                "description": "The location of the event"
            },
            "visibility": {
                "type": "string",
                "description": "The visibility of the event (default, public, private, confidential)"
            },
            "attendee_emails": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "The list of attendee emails. Must be valid email addresses"
            }
        },
        "required": ["summary", "start_datetime", "end_datetime"]
    }
)

async def serve() -> None:
    """Start the MCP server for the Arcade agent."""
    logger.info("Starting Arcade Agent MCP Server")
    
    # Check for API key and user ID
    api_key = os.getenv("ARCADE_API_KEY")
    user_id = os.getenv("ARCADE_USER_ID")
    
    if not api_key:
        logger.warning("ARCADE_API_KEY environment variable not set. Some features may be limited.")
    
    if not user_id:
        logger.warning("ARCADE_USER_ID environment variable not set. Some features may be limited.")
    
    # Create the MCP server
    server = Server("arcade-agent")
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """Register all available tools with the MCP server."""
        return [CREATE_EVENT_TOOL]
    
    @server.call_tool("create_event")
    async def call_create_event(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle calls to the 'create_event' tool."""
        logger.info(f"Received call to 'create_event' tool with parameters: {parameters}")
        return create_event(parameters)
    
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
        logger.info("Arcade Agent MCP Server shutting down.")

if __name__ == "__main__":
    # Run the server
    asyncio.run(serve()) 