"""
Standalone example to test Arcade API connectivity.
"""

import os
from dotenv import load_dotenv
from arcadepy import Arcade

# Load environment variables from .env file
load_dotenv()

def test_arcade_connection():
    """Test connectivity to Arcade API."""
    try:
        # Get API key from environment
        api_key = os.getenv("ARCADE_API_KEY")
        
        if not api_key:
            print("Error: ARCADE_API_KEY not found in environment variables.")
            print("Make sure you've created a .env file with your API key.")
            return False
        
        # Initialize client
        client = Arcade(api_key=api_key)
        
        # Make a simple request
        response = client.chat.completions.create(
            messages=[{
                "role": "user", 
                "content": "Hello! Can you help me learn German? Say hello in German."
            }],
        )
        
        # Print the response
        print("\n=== Arcade API Test ===")
        print(f"Response content: {response.choices[0].message.content}")
        print("=====================\n")
        
        return True
        
    except Exception as e:
        print(f"Error connecting to Arcade API: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Arcade API connection...")
    success = test_arcade_connection()
    print(f"Test {'succeeded' if success else 'failed'}") 