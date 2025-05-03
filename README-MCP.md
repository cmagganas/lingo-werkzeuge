# MCP Integration for Language Learning Tools

This project implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) to create a voice-controlled calendar assistant for language learning. It demonstrates how to use MCP to connect different agents (Vapi for speech and Arcade for Google Calendar).

## Architecture

The project follows the Model Context Protocol architecture:

1. **MCP Servers**: Each agent (Vapi and Arcade) is implemented as an MCP server that exposes specific tools.
2. **MCP Tools**: Each server exposes specialized tools that can be called by clients.
3. **Bridge**: The orchestrator bridges the two servers, allowing them to work together.

## Components

### Vapi Agent

The Vapi agent provides text-to-speech and speech-to-text capabilities using the Vapi API with Rime AI voices. It exposes these tools:

- **say_tool**: Convert text to speech using Rime AI voices
- **listen_tool**: Listen for speech and convert it to text
- **list_voices_tool**: List available Rime AI voices

### Arcade Agent

The Arcade agent provides integration with Google Workspace tools through the Arcade API. It exposes:

- **create_event_tool**: Create a new event/meeting in Google Calendar

### Chat Bridge

The chat bridge acts as an intermediary between the two agents, allowing users to:

1. Interact with the system using voice commands
2. Schedule calendar events with natural language
3. Receive voice feedback about the created events

## Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://astral.sh/uv) package manager (recommended)

### Installation

1. Create a virtual environment:

```bash
uv venv -p 3.10
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows
```

2. Install dependencies:

```bash
uv add "mcp[cli]" pydantic python-dotenv pyyaml vapi-python arcadepy httpx
```

3. Set up environment variables:

Create a `.env` file in the project root with:

```
# Vapi API key (for speech)
VAPI_API_KEY=your_vapi_api_key_here

# Arcade API credentials (for Google Calendar)
ARCADE_API_KEY=your_arcade_api_key_here
ARCADE_USER_ID=your_arcade_user_id_here
```

### Cursor Integration

To use these MCP servers with Cursor, copy the `cursor-mcp-config.json` to your Cursor configuration directory. The exact path depends on your operating system:

- **macOS/Linux**: `~/Library/Application Support/Cursor/cursor-mcp-config.json`
- **Windows**: `%APPDATA%\Cursor\cursor-mcp-config.json`

## Usage

### Running the Chat Bridge

To run the chat bridge in test mode (with simulated responses):

```bash
python src/orchestrator/chat_bridge.py --test-mode
```

To run with a specific voice:

```bash
python src/orchestrator/chat_bridge.py --voice elena
```

### Voice Commands

The chat bridge understands commands like:

- "Schedule a language learning study session tomorrow at 3 PM"
- "Create a meeting with my language tutor"
- "Exit" or "Goodbye" to exit

## MCP Server Details

### Server Configuration

The MCP servers are configured in `src/common/mcp_config.yaml` with:

```yaml
mcpServers:
  vapi-agent:
    command: python
    args: ["src/agents/vapi_agent/server.py"]
    env:
      VAPI_API_KEY: ${VAPI_API_KEY}
  
  arcade-agent:
    command: python
    args: ["src/agents/arcade_agent/server.py"]
    env:
      ARCADE_API_KEY: ${ARCADE_API_KEY}
      ARCADE_USER_ID: ${ARCADE_USER_ID}
```

### Tool Implementation

Tools are implemented using the FastMCP pattern from the MCP Python SDK:

```python
@mcp.tool()
async def tool_name(param1: str, param2: int = 42) -> Dict[str, Any]:
    """
    Tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    """
    # Tool implementation here
```

## Future Improvements

- Implement actual MCP client communication in the bridge
- Add more Google Workspace tools via Arcade
- Add voice-based language learning exercises
- Use LLMs for more sophisticated NLP for understanding user requests

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Vapi API](https://vapi.ai/)
- [Arcade API](https://arcade.software/) 