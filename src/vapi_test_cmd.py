#!/usr/bin/env python3
"""
Command-line script for testing Vapi with Rime AI voices.
"""
import sys

try:
    # Try to import from lingo_werkzeuge
    from lingo_werkzeuge.vapi.cli import main
    main()
except ImportError:
    # Fallback to local imports
    print("Error: Could not import from lingo_werkzeuge.vapi package.")
    print("Trying local imports...")
    
    try:
        from vapi.test import test_assistant, list_rime_voices
        
        print("Vapi Assistant Test with Rime AI Voice")
        print("=====================================")
        
        # Show available voices
        voices = list_rime_voices()
        print()
        
        # Ask for voice selection
        default_voice = "samantha"
        voice_choice = input(f"Choose a voice (default: {default_voice}): ").strip() or default_voice
        
        # Run the test
        success = test_assistant(voice_id=voice_choice)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    
    except ImportError:
        print("Error: Could not import Vapi test modules.")
        print("Make sure you have installed the required packages.")
        sys.exit(1) 