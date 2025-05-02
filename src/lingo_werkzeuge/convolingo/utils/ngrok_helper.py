import subprocess
import logging
import time
import json
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)

def start_ngrok(port: int = 5000) -> Optional[str]:
    """
    Start ngrok tunnel to expose local port
    
    Args:
        port: Local port to expose
        
    Returns:
        str: Public ngrok URL or None if failed
    """
    try:
        # Check if ngrok is available
        result = subprocess.run(
            ["which", "ngrok"], 
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error("ngrok command not found. Please install ngrok first.")
            return None
        
        # Start ngrok process
        logger.info(f"Starting ngrok tunnel for port {port}...")
        process = subprocess.Popen(
            ["ngrok", "http", str(port), "--log=stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for ngrok to start
        time.sleep(3)
        
        # Get ngrok tunnel URLs from the API
        result = subprocess.run(
            ["curl", "-s", "http://localhost:4040/api/tunnels"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error("Failed to get ngrok tunnel information")
            return None
        
        # Parse ngrok tunnel info
        try:
            tunnels = json.loads(result.stdout)
            public_url = tunnels["tunnels"][0]["public_url"]
            logger.info(f"ngrok tunnel established: {public_url}")
            return public_url
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.error(f"Failed to parse ngrok tunnel information: {e}")
            logger.debug(f"ngrok API response: {result.stdout}")
            return None
            
    except Exception as e:
        logger.error(f"Error starting ngrok: {e}")
        return None

def stop_ngrok() -> bool:
    """
    Stop all ngrok tunnels
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Kill all ngrok processes
        subprocess.run(
            ["killall", "ngrok"],
            capture_output=True,
            text=True
        )
        logger.info("Stopped all ngrok tunnels")
        return True
    except Exception as e:
        logger.error(f"Error stopping ngrok: {e}")
        return False 