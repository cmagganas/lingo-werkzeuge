"""
Vapi API integration for voice-based applications.
This is a wrapper around the main implementation in lingo_werkzeuge.vapi.
"""

__version__ = "0.1.0"

try:
    # Import functionality from lingo_werkzeuge package
    from lingo_werkzeuge.vapi import test_assistant, list_rime_voices
except ImportError:
    # Provide a fallback if the package isn't installed
    from .test import test_assistant, list_rime_voices 