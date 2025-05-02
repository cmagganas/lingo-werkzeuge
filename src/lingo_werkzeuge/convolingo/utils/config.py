import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any

# Set up logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_TARGET_LANGUAGE = "Spanish"
DEFAULT_ORIGIN_LANGUAGE = "English"
DEFAULT_CHAPTER = """
Chapter 1: Basic Greetings and Introductions

In this chapter, we'll cover:
1. Greeting people at different times of day
2. Introducing yourself and asking someone's name
3. Basic courtesies (please, thank you, you're welcome)
4. Saying goodbye

Start with a simple greeting and introduce yourself. 
Ask the student their name and what they know about the language already.
Guide them through basic greeting phrases.
Correct their pronunciation and grammar when needed.
Keep encouragement high and make it fun!
"""

WEBHOOK_PORT = 5000
DEFAULT_CONFIG_PATH = Path.home() / ".convolingo" / "config.env"

class Config:
    """Configuration singleton for ConvoLingo"""
    
    def __init__(self):
        """Initialize with default values"""
        # API configuration
        self.api_key = ""
        self.api_base = "https://api.vapi.ai"
        
        # Voice configuration
        self.voice_provider = "rime-ai"
        self.voice_id = "samantha"  # Default Rime AI voice
        
        # General configuration
        self.log_level = "INFO"
        self.log_dir = Path.home() / ".convolingo" / "logs"
        self.data_dir = Path.home() / ".convolingo" / "data"
        
        # Ensure directories exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration from environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Try to load from .env file if exists
        env_path = os.environ.get("CONVOLINGO_ENV_PATH", str(DEFAULT_CONFIG_PATH))
        if os.path.exists(env_path):
            logger.info(f"Loading configuration from {env_path}")
            load_dotenv(env_path)
        
        # API configuration
        self.api_key = os.environ.get("VAPI_API_KEY", self.api_key)
        self.api_base = os.environ.get("VAPI_API_BASE", self.api_base)
        
        # Voice configuration
        self.voice_provider = os.environ.get("VAPI_VOICE_PROVIDER", self.voice_provider)
        self.voice_id = os.environ.get("VAPI_VOICE_ID", self.voice_id)
        
        # General configuration
        self.log_level = os.environ.get("CONVOLINGO_LOG_LEVEL", self.log_level)
        
        # Convert string paths to Path objects
        log_dir = os.environ.get("CONVOLINGO_LOG_DIR")
        if log_dir:
            self.log_dir = Path(log_dir)
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
        data_dir = os.environ.get("CONVOLINGO_DATA_DIR")
        if data_dir:
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)

def load_config(config_path: Optional[str] = None) -> None:
    """
    Load configuration from specified path
    
    Args:
        config_path: Path to configuration file
    """
    if config_path:
        path = Path(config_path)
        if path.exists():
            logger.info(f"Loading configuration from {path}")
            load_dotenv(path)
            # Reload the configuration
            config._load_from_env()
        else:
            logger.warning(f"Configuration file not found: {path}")
    
# Create singleton instance
config = Config() 