# Voice-Enabled Calendar Assistant Setup Guide

This guide will help you set up and run the voice-enabled calendar assistant that allows you to schedule events using natural language commands.

## Prerequisites

1. A valid Vapi API key (get one from [https://vapi.ai](https://vapi.ai))
2. Python 3.8+
3. A microphone connected to your computer

## Installation

1. Install the required packages:
   ```bash
   pip install "mcp[cli]" python-dotenv pyyaml vapi-python
   ```

2. Set up your API keys:
   ```bash
   export VAPI_API_KEY=your_vapi_public_key
   ```

## Running the Voice Assistant

To run the assistant with voice capabilities:

```bash
cd lingo-werkzeuge
python3 src/orchestrator/direct_mcp_connect.py --start-servers --voice-input
```

Available command-line options:
- `--start-servers`: Start the MCP servers automatically
- `--voice-input`: Enable listening through the microphone
- `--voice [name]`: Choose a voice (default: samantha)
- `--debug`: Show more detailed logs
- `--test-mode`: Run in test mode with simulated input

## Supported Voices

You can use the following Rime AI voices:
- `samantha`: Female, clear and professional (default)
- `elena`: Female, warm and friendly
- `nicholas`: Male, authoritative and clear
- `tyler`: Male, conversational and friendly
- `maya`: Female, younger sounding voice
- `ally`: Female, energetic and upbeat

Example:
```bash
python3 src/orchestrator/direct_mcp_connect.py --start-servers --voice elena
```

## Example Commands

Here are some commands you can try saying:
- "Schedule a language learning session tomorrow at 3 PM"
- "Create a Spanish lesson for next Monday at 10 AM"
- "Set up a vocabulary review meeting on Friday at 2 PM"
- "Add a pronunciation practice at 9 AM"

## Troubleshooting

1. **API Key Issues**: 
   - Make sure you're using the public Vapi API key, not the private key
   - Check that the API key is exported in your terminal session

2. **Voice Input Not Working**:
   - Check that your microphone is connected and working
   - Try running with the `--debug` flag for more detailed error messages
   - Ensure you have permissions for microphone access

3. **Server Connection Issues**:
   - If you see "Connection refused" errors, ensure no other instances are running
   - Try killing any background processes with `pkill -f "python3 src/agents"`

4. **Crashes or Unexpected Errors**:
   - Check the logs for specific error messages
   - Try running without the `--voice-input` flag to test in text mode first

## How It Works

The system consists of three main components:

1. **Vapi Integration**: Handles speech-to-text and text-to-speech using Rime AI voices
2. **Arcade Agent**: Provides Google Calendar integration (simulated in this demo)
3. **Orchestrator**: Connects the components and manages the conversation flow

The `direct_mcp_connect.py` script starts these components and handles the interaction between them. 