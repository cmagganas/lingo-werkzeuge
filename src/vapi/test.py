#!/usr/bin/env python3
"""
Test module for Vapi integration with Rime AI voices.
This is a wrapper around the main implementation in lingo_werkzeuge.vapi.
"""
import sys

# Import functionality from lingo_werkzeuge package
try:
    from lingo_werkzeuge.vapi.test import test_assistant, list_rime_voices
    
    if __name__ == "__main__":
        """Run the test when script is executed directly"""
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
    print("Error: Could not import from lingo_werkzeuge.vapi package.")
    print("Make sure the package is properly installed.")
    sys.exit(1) 