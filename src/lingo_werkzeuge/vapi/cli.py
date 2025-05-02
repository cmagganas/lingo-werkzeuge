#!/usr/bin/env python3
"""
Command-line interface for testing Vapi with Rime AI voices.
"""
import argparse
import sys
from .test import test_assistant, list_rime_voices

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="Test Vapi with Rime AI voices"
    )
    
    # Add command line arguments
    parser.add_argument(
        "--voice", "-v", 
        default="samantha",
        help="Rime AI voice to use (default: samantha)"
    )
    parser.add_argument(
        "--message", "-m", 
        default="Hello, how are you today?",
        help="Test message to send to the assistant"
    )
    parser.add_argument(
        "--wait", "-w", 
        type=int,
        default=10,
        help="Time to wait for response in seconds (default: 10)"
    )
    parser.add_argument(
        "--list-voices", "-l",
        action="store_true",
        help="List available Rime AI voices"
    )
    
    args = parser.parse_args()
    
    # If just listing voices, do that and exit
    if args.list_voices:
        list_rime_voices()
        sys.exit(0)
    
    # Run the test
    print(f"Testing Vapi with Rime AI voice: {args.voice}")
    success = test_assistant(
        voice_id=args.voice,
        test_message=args.message,
        wait_time=args.wait
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 