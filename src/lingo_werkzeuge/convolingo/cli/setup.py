import os
import sys
import logging
from pathlib import Path
from typing import Optional

from lingo_werkzeuge.convolingo.utils.config import config, DEFAULT_CONFIG_PATH
from lingo_werkzeuge.convolingo.utils.logging_setup import setup_logging

# Set up logging
logger = setup_logging(__name__)

def setup_config(
    api_key: Optional[str] = None,
    voice_id: Optional[str] = None,
    config_path: Optional[str] = None
) -> bool:
    """
    Set up the configuration file
    
    Args:
        api_key: VAPI API key
        voice_id: Rime AI voice ID to use
        config_path: Path to the configuration file
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Setting up ConvoLingo configuration")
    
    # Determine config path
    if config_path:
        path = Path(config_path)
    else:
        path = Path(DEFAULT_CONFIG_PATH)
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get API key if not provided
    if not api_key:
        api_key = os.environ.get("VAPI_API_KEY")
        if not api_key:
            api_key = input("Enter your VAPI API key: ")
    
    # Get voice ID if not provided
    if not voice_id:
        voice_id = os.environ.get("VAPI_VOICE_ID")
        if not voice_id:
            print("\nAvailable Rime AI Voices:")
            print("1. samantha (default) - Female, clear and professional")
            print("2. elena - Female, warm and friendly")
            print("3. nicholas - Male, authoritative and clear")
            print("4. tyler - Male, conversational and friendly")
            print("5. maya - Female, younger sounding voice")
            print("6. ally - Female, energetic and upbeat")
            
            voice_choice = input("\nChoose a voice (1-6) or enter a custom Rime AI voice ID: ")
            
            # Map the choice to a voice ID
            voice_map = {
                "1": "samantha",
                "2": "elena",
                "3": "nicholas", 
                "4": "tyler",
                "5": "maya",
                "6": "ally"
            }
            
            voice_id = voice_map.get(voice_choice, voice_choice)
    
    # Create the configuration file
    try:
        with open(path, 'w') as f:
            f.write(f"# ConvoLingo Configuration\n")
            f.write(f"VAPI_API_KEY={api_key}\n")
            f.write(f"VAPI_API_BASE=https://api.vapi.ai\n")
            f.write(f"VAPI_VOICE_PROVIDER=rime-ai\n")
            f.write(f"VAPI_VOICE_ID={voice_id}\n")
            f.write(f"CONVOLINGO_LOG_LEVEL=INFO\n")
        
        logger.info(f"Configuration saved to {path}")
        print(f"\nConfiguration saved to {path}")
        print("You can modify this file directly to change settings.")
        return True
        
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        print(f"Error saving configuration: {e}")
        return False

def run_setup() -> None:
    """
    Run the interactive setup process
    """
    print("\n=================================================")
    print("  Welcome to ConvoLingo Setup!")
    print("=================================================\n")
    print("This will help you configure ConvoLingo for first use.\n")
    
    # Check if configuration already exists
    if Path(DEFAULT_CONFIG_PATH).exists():
        overwrite = input("Configuration file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Setup cancelled. Using existing configuration.")
            return
    
    # Get VAPI API key
    print("\nYou'll need a VAPI API key. Get one at https://vapi.ai")
    api_key = input("Enter your VAPI API key: ")
    
    # Choose voice
    print("\nChoose a Rime AI voice for your language assistant:")
    print("1. samantha (default) - Female, clear and professional")
    print("2. elena - Female, warm and friendly")
    print("3. nicholas - Male, authoritative and clear")
    print("4. tyler - Male, conversational and friendly")
    print("5. maya - Female, younger sounding voice")
    print("6. ally - Female, energetic and upbeat")
    
    voice_choice = input("\nChoose a voice (1-6) or enter a custom Rime AI voice ID: ")
    
    # Map the choice to a voice ID
    voice_map = {
        "1": "samantha",
        "2": "elena",
        "3": "nicholas", 
        "4": "tyler",
        "5": "maya",
        "6": "ally"
    }
    
    voice_id = voice_map.get(voice_choice, voice_choice)
    
    # Save configuration
    if setup_config(api_key, voice_id):
        print("\nSetup complete! You can now run ConvoLingo.")
    else:
        print("\nSetup failed. Please try again.")

if __name__ == "__main__":
    # This can be run directly for testing
    run_setup() 