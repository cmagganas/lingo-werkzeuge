# MCP Agents for Language Learning Tools

This directory contains MCP (Model Context Protocol) agents that can be used to integrate various tools and services with language learning applications.

## Available Agents

### Vapi Agent

The Vapi agent provides text-to-speech and speech-to-text capabilities using the Vapi API with Rime AI voices. It exposes the following tools:

- **say**: Convert text to speech using Rime AI voices
- **listen**: Listen for speech and convert it to text
- **list_voices**: List available Rime AI voices

### Arcade Agent

The Arcade agent provides integration with Google Workspace tools through the Arcade API. It exposes the following tools:

- **create_event**: Create a new event/meeting in Google Calendar

## Environment Setup

Create a `.env` file in the project root with the following variables:

```
# Vapi API key (for speech)
VAPI_API_KEY=your_vapi_api_key_here

# Arcade API credentials (for Google Calendar)
ARCADE_API_KEY=your_arcade_api_key_here
ARCADE_USER_ID=your_arcade_user_id_here
```

## Usage

### Running the Agents Individually

To run the Vapi agent:

```bash
python lingo-werkzeuge/src/agents/vapi_agent/server.py
```

To run the Arcade agent:

```bash
python lingo-werkzeuge/src/agents/arcade_agent/server.py
```

### Using the Orchestrator

The orchestrator bridges the two agents, allowing for voice-controlled calendar management:

```bash
python lingo-werkzeuge/src/orchestrator/chat_bridge.py --voice samantha
```

For testing purposes, you can use the `--test-mode` flag:

```bash
python lingo-werkzeuge/src/orchestrator/chat_bridge.py --test-mode
```

## Available Rime AI Voices

| Voice ID | Description | Gender |
|----------|-------------|--------|
| samantha | Clear and professional | Female |
| elena | Warm and friendly | Female |
| nicholas | Authoritative and clear | Male |
| tyler | Conversational and friendly | Male |
| maya | Younger sounding voice | Female |
| ally | Energetic and upbeat | Female |

## Project Structure

```
agents/
├── vapi_agent/           # Vapi MCP agent
│   ├── server.py         # Main MCP server
│   └── tools/            # Tools implementation
│       ├── say.py        # Text-to-speech
│       ├── listen.py     # Speech-to-text
│       └── list_voices.py # Voice listing
├── arcade_agent/         # Arcade MCP agent
│   ├── server.py         # Main MCP server
│   └── tools/            # Tools implementation
│       └── create_event.py # Calendar event creation
└── README.md             # This documentation
```

## Dependencies

- Python 3.9+
- mcp
- pydantic
- python-dotenv
- vapi-python-sdk (for Vapi agent)
- arcadepy (for Arcade agent)

## Future Extensions

- Adding more calendar management tools (delete events, list events, etc.)
- Email integration through Arcade
- More sophisticated natural language processing for request parsing
- Voice-based language learning exercises 