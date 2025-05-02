"""
Lingo Werkzeuge - An AI language learning assistant.
"""

__version__ = "0.1.0"

def main() -> None:
    """Entry point for the application"""
    from lingo_werkzeuge.convolingo.__main__ import main as convolingo_main
    convolingo_main()
