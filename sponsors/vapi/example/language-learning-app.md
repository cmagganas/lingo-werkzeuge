# Project Context

## Directory Structure

```bash
.
├── README.md
├── setup.py
├── .gitignore
├── .cursorrules
├── convolingo/
│   ├── __main__.py
│   ├── requirements.txt
│   ├── __init__.py
│   ├── api/
│   │   ├── client.py
│   │   ├── server.py
│   │   └── __init__.py
│   ├── tools/
│   │   ├── vocabulary.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── logging_setup.py
│   │   ├── ngrok_helper.py
│   │   └── __init__.py
│   └── cli/
│       ├── session.py
│       ├── interactive.py
│       ├── setup.py
│       └── __init__.py
├── build/
├── venv/
├── __pycache__/
└── conversation_history/
```

---

## File Contents

### README.md

```bash
# ConvoLingo - Talk and Learn New Languages! 🗣️🌍

ConvoLingo is a fun app that helps you learn new languages by talking with an AI teacher!
...
MIT - That means it's free to use and share! 
```

### setup.py

```python
from setuptools import setup, find_packages
import os
...
    options={
        'egg_info': {
            'egg_base': 'build',
        },
    },
) 
```

### convolingo/__main__.py

```python
import argparse
import sys
import logging
...
if __name__ == "__main__":
    main() 
```

### convolingo/api/client.py

```python
import time
import logging
import requests
from typing import Callable, Optional

from vapi_python import Vapi
from convolingo.utils.config import (
    config, DEFAULT_TARGET_LANGUAGE, 
    DEFAULT_ORIGIN_LANGUAGE, DEFAULT_CHAPTER
)

# Set up logging
logger = logging.getLogger(__name__)

# Constants for vocabulary tool creation
TOOL_NAME = 'vocabularyTool'
TOOL_DESCRIPTION = 'Tool to add, review and search vocabulary words'
TOOL_PARAMETERS = {
    "type": "object",
    "required": ["action"],
    "properties": {
        "word": {
            "type": "string",
            "description": "The vocabulary word to add or search for"
        },
        "action": {
            "type": "string",
            "description": "The action to perform (add, list, search)"
        },
        "language": {
            "type": "string",
            "description": "The language the word is in"
        },
        "translation": {
            "type": "string",
            "description": "The translation of the word"
        },
        "notes": {
            "type": "string",
            "description": "Additional notes about the word"
        }
    }
}


class VapiClient:
    """Client for interacting with the VAPI service"""
    
    def __init__(self):
        """Initialize the VAPI client"""
        self.client = None
        self.is_connected = False
        self.vocabulary_tool_id = None
    
    def _create_vocabulary_tool(self) -> Optional[str]:
        """
        Create a new vocabulary tool in VAPI
        
        Returns:
            str: Tool ID if successful, None otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            }
            
            # Create the tool - note the correct endpoint is /tool (singular)
            payload = {
                "type": "function",  # Specify the type as function
                "function": {
                    "name": TOOL_NAME,
                    "description": TOOL_DESCRIPTION,
                    "parameters": TOOL_PARAMETERS
                }
            }
            
            response = requests.post(
                f"{config.api_base}/tool",  # Fixed endpoint from /tools to /tool
                headers=headers,
                json=payload
            )
            
            if response.status_code == 201:
                data = response.json()
                tool_id = data.get("id")
                logger.info(f"Vocabulary tool created with ID: {tool_id}")
                return tool_id
            else:
                logger.error(
                    f"Failed to create tool: {response.status_code} {response.text}"
                )
                # Continue without the tool if creation fails
                return None
        except Exception as e:
            logger.error(f"Error creating vocabulary tool: {e}")
            # Continue without the tool if an exception occurs
            return None
    
    def connect(
        self, 
        target_language: str = DEFAULT_TARGET_LANGUAGE,
        native_language: str = DEFAULT_ORIGIN_LANGUAGE,
        chapter: str = DEFAULT_CHAPTER,
        user_id: Optional[str] = None,
    ) -> bool:
        """
        Connect to the VAPI service
        
        Args:
            target_language: The language to learn
            native_language: The user's native language
            chapter: The current chapter or module being studied
            user_id: Optional user ID for personalization
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Initialize VAPI client
            self.client = Vapi(api_key=config.api_key)
            
            # Log the configuration being sent
            logger.info(
                f"Connecting with: target={target_language}, "
                f"native={native_language}, chapter='{chapter[:30]}...'"
            )
            
            # Create the system prompt with the dynamic variables
            system_prompt = (
                "You are a language learning teaching assistant named Emma.\n"
                "You will begin a lesson plan starting in {native_language} "
                "and begin role playing speaking in {target_language}.\n\n"
                "native_language = \"{native_language}\"\n"
                "target_language = \"{target_language}\"\n\n"
                "{chapter}"
            ).format(
                native_language=native_language,
                target_language=target_language,
                chapter=chapter
            )
            
            # Create a custom assistant configuration
            assistant = {
                "model": {
                    "model": "gpt-3.5-turbo", 
                    "provider": "openai",
                    "temperature": 0.7,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        }
                    ]
                },
                "voice": {
                    "model": "eleven_multilingual_v2",
                    "voiceId": "S9EGwlCtMF7VXtENq79v",
                    "provider": "11labs",
                    "stability": 0.5,
                    "similarityBoost": 0.75
                },
                "transcriber": {
                    "model": "nova-3",
                    "language": "en-US",
                    "provider": "deepgram"
                }
            }
            
            # Add user ID if provided
            if user_id:
                assistant["userId"] = user_id
            
            # Use the assistant directly
            self.client.start(assistant=assistant)
            logger.info(f"Created custom assistant with chapter: {chapter}")
            
            self.is_connected = True
            logger.info(
                f"Connected to VAPI assistant for {target_language} learning"
            )
            return True
            
        except Exception as e:
            logger.error(f"Error connecting to VAPI: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the VAPI service"""
        if self.client and self.is_connected:
            try:
                self.client.stop()
                logger.info("Disconnected from VAPI assistant")
            except Exception as e:
                logger.error(f"Error disconnecting from VAPI: {e}")
            finally:
                self.is_connected = False
                self.client = None
    
    def send_message(self, text: str) -> bool:
        """
        Send a message to the assistant
        
        Args:
            text: The message text
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.client or not self.is_connected:
            logger.error("Cannot send message: Not connected to VAPI")
            return False
            
        try:
            # VAPI SDK method to send text
            # The exact method name may vary based on the SDK version
            # Try different methods that might be available
            if hasattr(self.client, 'send_text'):
                self.client.send_text(text)
            elif hasattr(self.client, 'user_message'):
                self.client.user_message(text)
            else:
                # Fallback - this might be the most recent one
                self.client.message(text)
            return True
        except Exception as e:
            logger.error(f"Error sending message to VAPI: {e}")
            return False
    
    def maintain_connection(self, should_continue: Callable[[], bool]) -> None:
        """
        Keep the connection alive until should_continue returns False
        
        Args:
            should_continue: Function that returns False when connection 
                             should end
        """
        try:
            while should_continue() and self.is_connected:
                time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error maintaining connection: {e}")
        finally:
            self.disconnect()
```

### convolingo/api/server.py

```python
import logging
import json
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify

from convolingo.utils.config import WEBHOOK_PORT
from convolingo.tools.vocabulary import VocabularyTool

# Set up logging
logger = logging.getLogger(__name__)

class WebhookServer:
    """Server for handling webhooks and tool API endpoints"""
    
    def __init__(self):
        """Initialize the webhook server"""
        self.app = Flask(__name__)
        self.vocabulary_tool = VocabularyTool()
        self.port = WEBHOOK_PORT
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register Flask routes"""
        
        @self.app.route('/callbacks', methods=['POST'])
        def handle_callback():
            """Handle webhook callbacks from VAPI"""
            try:
                # Get the JSON data from the request
                data = request.json
                
                # Log the received data
                logger.info(f"Webhook callback received: {data.get('type', 'unknown')}")
                
                # If this is a tool call event, process it
                if data.get('type') == 'tool-call':
                    tool_id = data.get('toolId')
                    tool_input = data.get('input', {})
                    
                    logger.info(f"Tool call received - Tool ID: {tool_id}")
                    
                    # Process the tool call
                    if tool_id == self.vocabulary_tool.tool_id:
                        result = self.vocabulary_tool.handle_tool_call(
                            str(tool_input)
                        )
                        return jsonify({
                            "success": True,
                            "result": result
                        })
                
                # For any other event type, just acknowledge receipt
                return jsonify({"success": True})
                
            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                return jsonify({"success": False, "error": str(e)}), 500

        @self.app.route('/api/vocabulary', methods=['POST'])
        def handle_vocabulary():
            """Handle vocabulary tool calls from VAPI"""
            try:
                # Get the JSON data from the request
                data = request.json
                
                # Log the received data
                logger.info(f"Vocabulary tool call received")
                
                # Extract text to process if available
                text_to_process = ""
                if isinstance(data, dict):
                    text_to_process = data.get('text', '')
                
                # Process the tool call
                result = self.vocabulary_tool.handle_tool_call(text_to_process)
                
                # Return a response that VAPI would use
                return jsonify({
                    "success": True,
                    "result": result
                })
                
            except Exception as e:
                logger.error(f"Error processing vocabulary tool call: {e}")
                return jsonify({"success": False, "error": str(e)}), 500

        @self.app.route('/', methods=['GET', 'POST'])
        def home():
            """Simple home page to verify the server is running"""
            if request.method == 'POST':
                try:
                    data = request.json
                    logger.info("POST request to root endpoint")
                    return jsonify({"success": True})
                except Exception as e:
                    logger.error(f"Error processing root POST: {e}")
                    return jsonify({"success": False, "error": str(e)}), 500
            
            return """
            <html>
                <body>
                    <h1>ConvoLingo Webhook Server</h1>
                    <p>This server is ready to receive callbacks from VAPI.</p>
                    <p>Use ngrok to expose this server to the internet.</p>
                </body>
            </html>
            """
    
    def run(self, debug: bool = False) -> None:
        """
        Run the webhook server
        
        Args:
            debug: Whether to run in debug mode
        """
        logger.info(f"Starting webhook server on port {self.port}...")
        logger.info("To expose this server, run: ngrok http 5000")
        self.app.run(debug=debug, port=self.port) 

```

### convolingo/tools/vocabulary.py

```python
import logging
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
import os
from datetime import datetime
...
    def search_word(self, language: str, query: str) -> Dict[str, Any]:
        """
        Search for a word in the vocabulary
        ...
        return {
            "success": True,
            "message": f"Found {len(results)} matches for '{query}' in {language}",
            "results": results
        } 
```

### convolingo/utils/config.py

```python
import os
from pathlib import Path
from dotenv import load_dotenv
...
# Create singleton instance
config = Config() 
```

### convolingo/utils/logging_setup.py

```python
import logging
import os
from pathlib import Path
from typing import Optional
...
def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name
    ...
    return logging.getLogger(name) 
```
