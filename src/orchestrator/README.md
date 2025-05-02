# Orchestrator for MCP Agents

This directory contains the orchestrator components that bridge multiple MCP agents together.

## Chat Bridge

The `chat_bridge.py` script connects the Vapi agent (speech) and Arcade agent (Google Calendar) to enable voice-controlled calendar management.

### Features

- Voice-based interaction through Vapi's Rime AI voices
- Natural language calendar event creation
- Simple command detection for scheduling events
- Test mode for simulating user input

### Usage

Run the chat bridge with the default voice:

```bash
python lingo-werkzeuge/src/orchestrator/chat_bridge.py
```

Specify a different voice:

```bash
python lingo-werkzeuge/src/orchestrator/chat_bridge.py --voice elena
```

Run in test mode to simulate user input:

```bash
python lingo-werkzeuge/src/orchestrator/chat_bridge.py --test-mode
```

### Voice Commands

The chat bridge understands the following types of commands:

- **Schedule an event**: "Schedule a language learning study session tomorrow at 3 PM"
- **Exit**: "Goodbye", "Exit", "Quit", "Stop"

### Architecture

The chat bridge acts as a mediator between the two MCP agents:

1. It initializes MCP clients for both the Vapi and Arcade agents
2. Listens for user speech input through the Vapi agent
3. Processes the speech to determine the user's intent
4. For scheduling requests, extracts event details and calls the Arcade agent
5. Provides voice feedback using the Vapi agent

### Dependencies

- mcp
- python-dotenv
- datetime, re (built-in)

### Future Improvements

- More sophisticated NLP for extracting event details
- Support for additional calendar operations (view, delete, update events)
- Multi-turn conversations for clarifying details
- Integration with language learning workflows 