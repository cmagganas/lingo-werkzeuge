import time
import logging
import requests
from typing import Callable, Optional, Dict, Any, List

from vapi import Vapi
from lingo_werkzeuge.convolingo.utils.config import (
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
        self.assistant_id = None
        self.active_call_id = None
    
    def _create_vocabulary_tool(self) -> Optional[str]:
        """
        Create a new vocabulary tool in VAPI
        
        Returns:
            str: Tool ID if successful, None otherwise
        """
        try:
            # Using the new client approach
            if not self.client:
                self.client = Vapi(token=config.api_key)
                
            # Create the tool using the new API method
            tool_data = {
                "type": "function",
                "function": {
                    "name": TOOL_NAME,
                    "description": TOOL_DESCRIPTION,
                    "parameters": TOOL_PARAMETERS
                }
            }
            
            response = self.client.tools.create(**tool_data)
            
            if response and "id" in response:
                tool_id = response["id"]
                logger.info(f"Vocabulary tool created with ID: {tool_id}")
                return tool_id
            else:
                logger.error("Failed to create tool: No ID returned")
                return None
        except Exception as e:
            logger.error(f"Error creating vocabulary tool: {e}")
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
            # Initialize VAPI client if not already done
            if not self.client:
                self.client = Vapi(token=config.api_key)
            
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
            assistant_data = {
                "name": "Language Learning Assistant",
                "model": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo", 
                    "temperature": 0.7,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        }
                    ]
                },
                "voice": {
                    "provider": "rime-ai",
                    "voiceId": config.voice_id,
                },
                "transcriber": {
                    "provider": "deepgram",
                    "model": "nova-3",
                    "language": "en-US",
                },
                "firstMessage": "Hello! I'm Emma, your language learning assistant. Let's start our lesson today."
            }
            
            # Add user ID metadata if provided
            if user_id:
                assistant_data["metadata"] = {"userId": user_id}
                
            # Create the assistant using the new API
            response = self.client.assistants.create(**assistant_data)
            
            if response and "assistantId" in response:
                self.assistant_id = response["assistantId"]
                logger.info(f"Created assistant with ID: {self.assistant_id}")
                
                # Start a call with the assistant
                call_response = self.client.calls.create(assistantId=self.assistant_id)
                
                if call_response and "callId" in call_response:
                    self.active_call_id = call_response["callId"]
                    logger.info(f"Started call with ID: {self.active_call_id}")
                    self.is_connected = True
                    logger.info(f"Connected to VAPI assistant for {target_language} learning")
                    return True
                else:
                    logger.error("Failed to start call: No ID returned")
                    return False
            else:
                logger.error("Failed to create assistant: No ID returned")
                return False
            
        except Exception as e:
            logger.error(f"Error connecting to VAPI: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self) -> None:
        """Disconnect from the VAPI service"""
        if self.client and self.is_connected:
            try:
                if self.active_call_id:
                    # End the active call
                    self.client.calls.end(callId=self.active_call_id)
                    logger.info(f"Ended call {self.active_call_id}")
                    self.active_call_id = None
                
                # Optional: Clean up the assistant if no longer needed
                # if self.assistant_id:
                #     self.client.assistants.delete(assistantId=self.assistant_id)
                #     logger.info(f"Deleted assistant {self.assistant_id}")
                #     self.assistant_id = None
                
                logger.info("Disconnected from VAPI assistant")
            except Exception as e:
                logger.error(f"Error disconnecting from VAPI: {e}")
            finally:
                self.is_connected = False
    
    def send_message(self, text: str) -> bool:
        """
        Send a message to the assistant
        
        Args:
            text: The message text
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        if not self.client or not self.is_connected or not self.active_call_id:
            logger.error("Cannot send message: Not connected to VAPI")
            return False
            
        try:
            # Send message to the active call
            self.client.calls.send_text(callId=self.active_call_id, text=text)
            logger.info(f"Sent message to call {self.active_call_id}")
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
                
            if self.is_connected:
                # End the active call
                if self.active_call_id:
                    self.client.calls.end(callId=self.active_call_id)
                    logger.info(f"Ended call {self.active_call_id}")
                    self.active_call_id = None
        except Exception as e:
            logger.error(f"Error maintaining connection: {e}")
        finally:
            self.disconnect() 