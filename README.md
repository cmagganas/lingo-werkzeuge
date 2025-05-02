# Lingo Werkzeuge

An interactive AI-powered language learning assistant demo app, showcasing integration with sponsor SDKs and best practices for project setup.

## Features

- 🗣️ **Interactive Language Learning** - Practice conversations with an AI tutor
- 🌍 **Multiple Language Support** - Learn Spanish, French, and many other languages
- 🎙️ **Natural Voice Synthesis** - Lifelike speech using Rime AI voices
- 📚 **Vocabulary Management** - Save and review words you learn
- 🧠 **Intelligent Tutoring** - AI adapts to your learning needs

## Architecture

Project file structure:

```bash
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # This file
├── .env                   # Environment variables and API keys
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
```

## Installation

```bash
# Clone the repository
git clone https://github.com/cmagganas/lingo-werkzeuge.git
cd lingo-werkzeuge

# Create and activate a virtual environment
uv venv .venv
source .venv/bin/activate

# Install dependencies
uv add vapi_python flask python-dotenv requests pydantic
```

## Environment Variables

Create a `.env` file with your API keys:

```bash
# Vapi API credentials
VAPI_API_KEY=your_vapi_api_key_here

# Voice configuration (using Rime AI)
VAPI_VOICE_PROVIDER=rime-ai
VAPI_VOICE_ID=samantha  # Options: samantha, elena, maya, ally, nicholas, tyler

# Other API keys
OPENAI_API_KEY=your_openai_api_key_here
ARCADE_API_KEY=your_arcade_api_key_here
```

## Usage

### Testing Vapi with Rime AI Voices

You can test the Vapi integration with Rime AI voices using one of the following commands:

```bash
# List available Rime AI voices
python -m lingo_werkzeuge.vapi.cli --list-voices

# Test with the default voice (samantha)
python -m lingo_werkzeuge.vapi.cli

# Test with a specific voice
python -m lingo_werkzeuge.vapi.cli --voice elena

# Test with a custom message and longer wait time
python -m lingo_werkzeuge.vapi.cli --voice nicholas --message "Tell me about language learning" --wait 15
```

### Running the Language Learning Application

The full language learning application can be run with:

```bash
# Start the main application
python -m lingo_werkzeuge

# Start with a specific language
python -m lingo_werkzeuge --language French

# Start with debug logging
python -m lingo_werkzeuge --debug
```

## Available Rime AI Voices

The application supports multiple Rime AI voices:

- `samantha` - Female, clear and professional (default)
- `elena` - Female, warm and friendly
- `nicholas` - Male, authoritative and clear
- `tyler` - Male, conversational and friendly
- `maya` - Female, younger sounding voice
- `ally` - Female, energetic and upbeat

## Project Structure Overview

### Main Components

1. **ConvoLingo** - The core language learning application
   - Interactive CLI for language practice
   - Vocabulary management tools
   - Webhook server for API integrations

2. **Vapi Integration** - Voice synthesis using Vapi and Rime AI
   - Testing utilities and CLI for Vapi
   - Voice selection and configuration
   - Speech synthesis with natural-sounding voices

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Vapi](https://vapi.ai) - For their voice conversation API
- [Rime AI](https://docs.vapi.ai/providers/voice/rimeai) - For their natural-sounding voices
- [Arcade](https://arcade.software) - For their AI SDK
- Other sponsors of the MCP hackathon
