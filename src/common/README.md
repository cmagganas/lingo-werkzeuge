# Common Utilities for MCP Agents

This directory contains common utilities and configuration files used by multiple MCP agents.

## Files

- **mcp_config.yaml**: Configuration for MCP servers, used by Cursor for launching agents
- **utils.py**: Shared utility functions used across agent implementations

## MCP Configuration

The `mcp_config.yaml` file defines the server configurations for each MCP agent. This allows Cursor to launch the agents with the correct command, arguments, and environment variables.

Example:

```yaml
mcpServers:
  vapi-agent:
    command: python
    args: ["lingo-werkzeuge/src/agents/vapi_agent/server.py"]
    env:
      VAPI_API_KEY: ${VAPI_API_KEY}
  
  arcade-agent:
    command: python
    args: ["lingo-werkzeuge/src/agents/arcade_agent/server.py"]
    env:
      ARCADE_API_KEY: ${ARCADE_API_KEY}
      ARCADE_USER_ID: ${ARCADE_USER_ID}
```

## Utility Functions

The `utils.py` file provides shared functionality:

- **init_mcp_client**: Initializes an MCP client for a given agent using the configuration from `mcp_config.yaml`

### Usage

```python
from common.utils import init_mcp_client

# Initialize an MCP client for the Vapi agent
vapi_client = init_mcp_client("vapi-agent")

# Use the client to execute a tool
result = vapi_client.execute("say", {
    "text": "Hello, world!",
    "voice_id": "samantha"
})
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Vapi API key (for speech)
VAPI_API_KEY=your_vapi_api_key_here

# Arcade API credentials (for Google Calendar)
ARCADE_API_KEY=your_arcade_api_key_here
ARCADE_USER_ID=your_arcade_user_id_here 