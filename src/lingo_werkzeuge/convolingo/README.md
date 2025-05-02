# ConvoLingo

Talk and learn new languages with an AI assistant! 🗣️🌍

## Overview

ConvoLingo is an interactive language learning application that allows you to practice conversation in different languages with an AI language tutor. The tutor will guide you through lessons, correct your pronunciation and grammar, and help you build vocabulary as you learn.

## Features

- Interactive language learning conversations
- Support for multiple languages
- Vocabulary tool to save and review words
- Natural speech synthesis using Rime AI voices
- Customizable lesson content

## Installation

1. Make sure you have Python 3.8+ installed
2. Clone this repository
3. Install the package:

```bash
pip install -e .
```

4. Install the required dependencies:

```bash
pip install -r lingo_werkzeuge/convolingo/requirements.txt
```

## Setup

Before using ConvoLingo, you need to:

1. Create a VAPI account at [https://vapi.ai](https://vapi.ai) and get an API key
2. Run the setup script:

```bash
python -m lingo_werkzeuge.convolingo.cli.setup
```

This will guide you through setting up your API key and choosing a voice for your language tutor.

## Usage

Start an interactive language learning session:

```bash
python -m lingo_werkzeuge.convolingo
```

This will start a session with the default settings (learning Spanish).

### Command Line Options

Use the following options to customize your session:

- `--language` or `-l`: The target language to learn (default: Spanish)
- `--native` or `-n`: Your native language (default: English)
- `--config` or `-c`: Path to a custom configuration file
- `--debug` or `-d`: Enable debug logging

Example:

```bash
python -m lingo_werkzeuge.convolingo --language French --native English
```

## Voice Options

ConvoLingo uses Rime AI's voices for speech synthesis. Available voices include:

- `samantha` (default) - Female, clear and professional
- `elena` - Female, warm and friendly
- `nicholas` - Male, authoritative and clear
- `tyler` - Male, conversational and friendly
- `maya` - Female, younger sounding voice
- `ally` - Female, energetic and upbeat

You can choose your preferred voice during setup or modify it in your configuration file.

## Configuration

The default configuration file is located at `~/.convolingo/config.env`. You can edit this file directly to change settings.

## License

MIT License 