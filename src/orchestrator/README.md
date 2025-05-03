# Voice-Controlled Calendar Assistant

This is a voice-controlled assistant that allows scheduling events in your calendar using natural language commands. It bridges Vapi (a speech-to-text and text-to-speech service) with Arcade (Google Calendar integration).

## Setup

1. Make sure you have the required API keys:
   ```bash
   export VAPI_API_KEY=your_vapi_api_key
   export ARCADE_API_KEY=your_arcade_api_key
   export ARCADE_USER_ID=your_arcade_user_id
   ```

2. Install dependencies:
   ```bash
   pip install "mcp[cli]" python-dotenv pyyaml
   ```

## Running the System

You need to run three different components in separate terminals:

### Terminal 1: Start the Vapi Agent Server

```bash
cd /Users/christos/cmagganas/mcp-a2a-hackathon/lingo-werkzeuge
python3 src/agents/vapi_agent/server.py
```

### Terminal 2: Start the Arcade Agent Server

```bash
cd /Users/christos/cmagganas/mcp-a2a-hackathon/lingo-werkzeuge
python3 src/agents/arcade_agent/server.py
```

### Terminal 3: Start the Chat Bridge

```bash
cd /Users/christos/cmagganas/mcp-a2a-hackathon/lingo-werkzeuge
python3 src/orchestrator/chat_bridge.py
```

## Using the System

Once all three components are running:

1. You will hear a welcome message from the voice assistant
2. Speak into your microphone with commands like:
   - "Schedule a language learning session tomorrow at 3 PM"
   - "Create a meeting with John next Monday at 10 AM"
   - "Add a doctor's appointment for Friday at 2 PM"
3. The system will confirm the details and create the event in your calendar
4. To exit, say "goodbye" or "exit"

## Test Mode

If you want to test without using a real microphone:
```bash
python3 src/orchestrator/chat_bridge.py --test-mode
```

This will simulate voice input for testing purposes.

## Troubleshooting

- If you see connection errors, make sure all three servers are running and your API keys are set correctly
- Check the logs at WARNING level for errors
- If the logs are too verbose, you can modify the logging level in chat_bridge.py
- Make sure you're using python3 (not python) for all commands
- Verify that the `src/common/mcp_config.yaml` file exists and has the correct contents

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
python3 src/orchestrator/chat_bridge.py
```

Specify a different voice:

```bash
python3 src/orchestrator/chat_bridge.py --voice elena
```

Run in test mode to simulate user input:

```bash
python3 src/orchestrator/chat_bridge.py --test-mode
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
- pyyaml
- datetime, re (built-in)

### Future Improvements

- More sophisticated NLP for extracting event details
- Support for additional calendar operations (view, delete, update events)
- Multi-turn conversations for clarifying details
- Integration with language learning workflows 