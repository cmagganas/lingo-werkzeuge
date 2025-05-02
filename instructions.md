# Instructions

## Project Overview

Lingo Werkzeuge is a fun hackathon app that helps you learn new languages by talking with an AI teacher! It uses voice synthesis technology from Vapi and Rime AI to create natural-sounding conversations for an immersive language learning experience.

## Core Functionalities

1. **Interactive Language Learning** - Converse with an AI language tutor via voice
2. **Multiple Language Support** - Practice conversations in various languages
3. **Natural Voice Synthesis** - Lifelike speech using Rime AI voices
4. **Vocabulary Management** - Save and review words you learn
5. **Customizable Learning** - Tailor the learning experience to your needs

## Architecture

Project file structure:

```bash
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # Overview and installation instructions
├── .env                   # Environment variables and API keys (gitignored)
├── src/                   # Source code directory
│   ├── lingo_werkzeuge/   # Main package code
│   │   ├── __init__.py    # Package initialization
│   │   ├── convolingo/    # Language learning application
│   │   │   ├── __init__.py
│   │   │   ├── __main__.py
│   │   │   ├── api/       # API clients and server
│   │   │   ├── cli/       # Command-line interface
│   │   │   ├── tools/     # Language learning tools
│   │   │   └── utils/     # Utility functions
│   │   └── vapi/          # Vapi integration module
│   │       ├── __init__.py
│   │       ├── cli.py     # Command-line interface for testing
│   │       └── test.py    # Testing utilities for Vapi+Rime AI
│   ├── vapi/              # Direct-access test utilities
│   │   ├── __init__.py
│   │   └── test.py
│   └── vapi_test_cmd.py   # Command-line script for testing
├── docs                   # Documentation
├── hackathon              # Hackathon-specific information
└── sponsors               # Sponsor SDK documentation
    ├── arcade
    ├── arize
    ├── rime
    ├── senso
    └── vapi
        └── example
            └── language-learning-app.md  # Detailed implementation of the app
```

## Dependencies

- **Python**: 3.8+ (3.12 recommended)
- **vapi_python**: Vapi SDK for voice conversation APIs
- **flask**: Web framework for webhook server
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API requests
- **pydantic**: Data validation and settings management

## Documentation

### Vapi with Rime AI Integration

We've implemented a complete voice-based language learning application using Vapi's API with Rime AI voices:

1. **Voice Selection**: The app supports multiple Rime AI voices:
   - `samantha` - Female, clear and professional (default)

2. **Testing Utilities**: The project includes comprehensive testing utilities:
   - Command-line interface: `python -m lingo_werkzeuge.vapi.cli --voice samantha`
   - Direct testing: `python -m vapi.test`
   - Voice listing: `python -m lingo_werkzeuge.vapi.cli --list-voices`

3. **Configuration**: API keys and voice settings can be customized through:
   - Environment variables: `VAPI_API_KEY`, `VAPI_VOICE_ID`
   - `.env` file for persistent configuration

## Package Documentation & Examples

### Vapi

#### Installation

```bash
# Install Vapi SDK
uv add vapi_python

# Install required dependencies
uv add flask python-dotenv requests pydantic
```

#### Basic Usage with Rime AI Voice

```python
from vapi_python import Vapi
import os

# Initialize client with API key
client = Vapi(api_key=os.getenv("VAPI_API_KEY"))

# Create assistant configuration with Rime AI voice
assistant = {
    "model": {
        "model": "gpt-3.5-turbo", 
        "provider": "openai",
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant named Emma."
            }
        ]
    },
    "voice": {
        "provider": "rime-ai",
        "voiceId": "samantha",  # Rime AI voice
    },
    "transcriber": {
        "model": "nova-3",
        "language": "en-US",
        "provider": "deepgram"
    }
}

# Start a session with the assistant
client.start(assistant=assistant)

# Send a message
client.user_message("Hello, how are you today?")
```

### Arcade

#### Installation

```bash
uv add arcadepy
```

#### Quickstart Example

```python
import os
from arcadepy import Arcade

# Initialize client with API key from environment
client = Arcade(api_key=os.getenv("ARCADE_API_KEY"))

# Send a chat completion request
response = client.chat.completions.create(
    messages=[{"role": "user", "content": "Hello from Arcade!"}],
)
print(response)
```

### Rime, Arize, and Senso

Documentation and examples for these sponsors will be added as they're integrated.

## Resources & References

- [Vapi Documentation](https://docs.vapi.ai/)
- [Rime AI Voices Documentation](https://docs.vapi.ai/providers/voice/rimeai)
- [Vapi API Reference](https://docs.vapi.ai/api-reference/assistants/create#request.body.voice.rime-ai)

## Next Steps

- [x] Initialize project with `uv init --package lingo-werkzeuge`
- [x] Create and activate virtual environment: `uv venv .venv && source .venv/bin/activate`
- [x] Sync dependencies: `uv sync`
- [x] Install Vapi SDK: `uv add vapi_python`
- [x] Implement Vapi integration with Rime AI voices
- [x] Create testing utilities for Vapi
- [x] Document implementation in instructions.md
- [ ] Integrate additional sponsor SDKs (Arcade, etc.)
- [ ] Expand language learning application features
