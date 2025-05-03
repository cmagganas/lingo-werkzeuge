# Lingo-Werkzeuge: Voice-Controlled Calendar Assistant for Language Learning

This project connects two AI agents using the Model Context Protocol (MCP):
- **Vapi Agent**: Provides speech-to-text and text-to-speech capabilities
- **Arcade Agent**: Provides Google Calendar integration

## Setup

1. Make sure you have the required API keys:
   ```bash
   export VAPI_API_KEY=your_vapi_api_key
   export ARCADE_API_KEY=your_arcade_api_key
   export ARCADE_USER_ID=your_arcade_user_id
   ```

2. Install dependencies:
   ```bash
   pip install "mcp[cli]" python-dotenv pyyaml vapi-python
   ```

## Running the System

**Option 1: Voice-Enabled Assistant (Recommended)**

The most complete solution with real voice capabilities:

```bash
cd /Users/christos/cmagganas/mcp-a2a-hackathon/lingo-werkzeuge
python3 src/orchestrator/direct_mcp_connect.py --start-servers --voice-input
```

Command line options:
- `--start-servers`: Start the MCP servers automatically
- `--voice-input`: Enable listening through the microphone
- `--voice [name]`: Choose a voice (default: samantha)
- `--debug`: Show more detailed logs
- `--test-mode`: Run in test mode with simulated input

For detailed setup instructions, see [VOICE_SETUP.md](VOICE_SETUP.md).

**Option 2: Start the MCP Servers (separately)**

You need to run two servers in separate terminals:

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

### Terminal 3: Run the Connection Test

For a quick test that both agents are working correctly:

```bash
cd /Users/christos/cmagganas/mcp-a2a-hackathon/lingo-werkzeuge
python3 src/orchestrator/connect_to_agents.py --test-mode
```

**Option 3: Use the Simple Interactive Demo**

Skip the MCP complexity and run our interactive demo:

```bash
cd /Users/christos/cmagganas/mcp-a2a-hackathon/lingo-werkzeuge
python3 demo.py
```

This will let you simulate voice commands by typing them, demonstrating how the system is designed to work.

## Using the Real System

Once all components are running:

1. You will hear a welcome message from the voice assistant
2. Speak into your microphone with commands like:
   - "Schedule a language learning session tomorrow at 3 PM"
   - "Create a meeting with my Spanish tutor next Monday at 10 AM" 
   - "Add a language study appointment for Friday at 2 PM"
3. The system will confirm the details and create the event in your calendar
4. To exit, say "goodbye" or "exit"

## Voice Capability

To use real voice capabilities with the improved implementation:
1. Make sure `VAPI_API_KEY` is set in your environment (use the public key)
2. Use the `direct_mcp_connect.py` script with both `--start-servers` and `--voice-input` options
3. Speak clearly into your microphone when prompted
4. If you encounter any issues, check the [VOICE_SETUP.md](VOICE_SETUP.md) troubleshooting guide

## Known Issues and Solutions

1. **Connection issues with chat_bridge.py**: 
   - The original implementation has issues connecting to running MCP servers
   - Use the `direct_mcp_connect.py` script instead, which uses the Vapi SDK directly

2. **Config file errors**: 
   - Make sure `src/common/mcp_config.yaml` exists and has the correct Python path
   
3. **Python path errors**:
   - Always use `python3` instead of `python` for all commands

4. **API key errors**:
   - Make sure your `VAPI_API_KEY` is correctly set and is the public key for Vapi
   - Double-check all environment variables are properly exported before running

## What We've Built

1. **MCP Servers**:
   - Vapi Agent for voice capabilities
   - Arcade Agent for Google Calendar integration
   
2. **Tools**:
   - **Vapi Tools**:
     - `say_tool`: Text-to-speech using Rime AI voices
     - `listen_tool`: Speech-to-text capabilities
     - `list_voices_tool`: Lists available Rime AI voices
   
   - **Arcade Tools**:
     - `create_event_tool`: Creates calendar events

3. **Integration Solutions**:
   - Multiple ways to run the system:
     - `direct_mcp_connect.py`: Direct integration with Vapi SDK for real voice support
     - `connect_to_agents.py`: Tests MCP servers via HTTP calls
     - `demo.py`: Simple simulation of the system
   
4. **Demo Application**:
   - Interactive demonstration of the system capabilities

## Troubleshooting

- If you see connection errors, make sure all servers are running and your API keys are set correctly
- Check the logs at WARNING level for errors
- If the logs are too verbose, modify the logging level in the Python files
- Make sure you're using python3 (not python) for all commands
- Verify that the `src/common/mcp_config.yaml` file exists and has the correct contents
