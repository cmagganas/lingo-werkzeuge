import argparse
import sys
import logging
import time
from pathlib import Path

from lingo_werkzeuge.convolingo.utils.logging_setup import setup_logging
from lingo_werkzeuge.convolingo.utils.config import config, load_config
from lingo_werkzeuge.convolingo.cli.interactive import start_interactive_session

# Set up logging
logger = setup_logging(__name__)

def main():
    """Main entry point for the ConvoLingo application"""
    parser = argparse.ArgumentParser(
        description="ConvoLingo - Talk and Learn New Languages!"
    )
    
    # Add command line arguments
    parser.add_argument(
        "--language", "-l", 
        default="Spanish",
        help="Target language to learn (default: Spanish)"
    )
    parser.add_argument(
        "--native", "-n", 
        default="English",
        help="Your native language (default: English)"
    )
    parser.add_argument(
        "--config", "-c",
        help="Path to custom configuration file"
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        
    # Load configuration
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            logger.error(f"Configuration file not found: {args.config}")
            sys.exit(1)
        load_config(args.config)
    
    logger.info(f"Starting ConvoLingo with target language: {args.language}")
    
    try:
        # Start interactive session
        start_interactive_session(
            target_language=args.language,
            native_language=args.native
        )
    except KeyboardInterrupt:
        logger.info("ConvoLingo session terminated by user")
    except Exception as e:
        logger.error(f"Error in ConvoLingo session: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    logger.info("ConvoLingo session ended")
    sys.exit(0)

if __name__ == "__main__":
    main() 