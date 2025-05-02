import os
import yaml
import logging
from typing import Optional
from mcp import MCPClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Constants
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "mcp_config.yaml")

def init_mcp_client(agent_name: str) -> MCPClient:
    """
    Initialize and return an MCPClient for the given agent_name using mcp_config.yaml.
    
    Args:
        agent_name (str): The name of the agent to initialize (e.g., "vapi-agent")
        
    Returns:
        MCPClient: An initialized MCP client for the specified agent
        
    Raises:
        KeyError: If no MCP server configuration is found for the agent
        FileNotFoundError: If the configuration file doesn't exist
    """
    try:
        # Load MCP server configurations
        with open(CONFIG_PATH) as f:
            config = yaml.safe_load(f)
            
        server_conf = config.get("mcpServers", {}).get(agent_name)
        if not server_conf:
            raise KeyError(f"No MCP server configuration found for agent '{agent_name}'")
            
        # Process environment variables in the config
        env = {}
        for key, value in server_conf.get("env", {}).items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                env[key] = os.environ.get(env_var, "")
            else:
                env[key] = value
                
        # Instantiate MCP client
        return MCPClient(
            command=server_conf["command"], 
            args=server_conf["args"],
            env=env
        )
        
    except FileNotFoundError:
        logger.error(f"Config file not found: {CONFIG_PATH}")
        raise
    except Exception as e:
        logger.error(f"Error initializing MCP client: {e}")
        raise 