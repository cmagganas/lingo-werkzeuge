import logging
import json
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify

from lingo_werkzeuge.convolingo.utils.config import WEBHOOK_PORT
from lingo_werkzeuge.convolingo.tools.vocabulary import VocabularyTool

# Set up logging
logger = logging.getLogger(__name__)

class WebhookServer:
    """Server for handling webhooks and tool API endpoints"""
    
    def __init__(self):
        """Initialize the webhook server"""
        self.app = Flask(__name__)
        self.vocabulary_tool = VocabularyTool()
        self.port = WEBHOOK_PORT
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self) -> None:
        """Register Flask routes"""
        
        @self.app.route('/callbacks', methods=['POST'])
        def handle_callback():
            """Handle webhook callbacks from VAPI"""
            try:
                # Get the JSON data from the request
                data = request.json
                
                # Log the received data
                logger.info(f"Webhook callback received: {data.get('type', 'unknown')}")
                
                # If this is a tool call event, process it
                if data.get('type') == 'tool-calls':
                    tool_calls = data.get('toolCalls', [])
                    
                    for tool_call in tool_calls:
                        tool_id = tool_call.get('id')
                        tool_name = tool_call.get('function', {}).get('name')
                        tool_arguments = tool_call.get('function', {}).get('arguments', {})
                        
                        logger.info(f"Tool call received - Tool: {tool_name}")
                        
                        # Process the tool call if it's our vocabulary tool
                        if tool_name == self.vocabulary_tool.tool_name:
                            result = self.vocabulary_tool.handle_tool_call(tool_arguments)
                            return jsonify({
                                "success": True,
                                "result": result
                            })
                
                # For any other event type, just acknowledge receipt
                return jsonify({"success": True})
                
            except Exception as e:
                logger.error(f"Error processing webhook: {e}")
                return jsonify({"success": False, "error": str(e)}), 500

        @self.app.route('/api/vocabulary', methods=['POST'])
        def handle_vocabulary():
            """Handle vocabulary tool calls from VAPI"""
            try:
                # Get the JSON data from the request
                data = request.json
                
                # Log the received data
                logger.info(f"Vocabulary tool call received")
                
                # Extract text to process if available
                action = ""
                word = ""
                language = ""
                translation = ""
                notes = ""
                
                if isinstance(data, dict):
                    action = data.get('action', '')
                    word = data.get('word', '')
                    language = data.get('language', '')
                    translation = data.get('translation', '')
                    notes = data.get('notes', '')
                
                # Process the tool call based on action
                if action == 'add':
                    result = self.vocabulary_tool.add_word(
                        language, word, translation, notes
                    )
                elif action == 'list':
                    result = self.vocabulary_tool.list_words(language)
                elif action == 'search':
                    result = self.vocabulary_tool.search_word(language, word)
                else:
                    result = {
                        "success": False,
                        "message": f"Unknown action: {action}"
                    }
                
                # Return a response that VAPI would use
                return jsonify({
                    "success": True,
                    "result": result
                })
                
            except Exception as e:
                logger.error(f"Error processing vocabulary tool call: {e}")
                return jsonify({"success": False, "error": str(e)}), 500

        @self.app.route('/', methods=['GET', 'POST'])
        def home():
            """Simple home page to verify the server is running"""
            if request.method == 'POST':
                try:
                    data = request.json
                    logger.info("POST request to root endpoint")
                    return jsonify({"success": True})
                except Exception as e:
                    logger.error(f"Error processing root POST: {e}")
                    return jsonify({"success": False, "error": str(e)}), 500
            
            return """
            <html>
                <body>
                    <h1>ConvoLingo Webhook Server</h1>
                    <p>This server is ready to receive callbacks from VAPI.</p>
                    <p>Use ngrok to expose this server to the internet.</p>
                </body>
            </html>
            """
    
    def run(self, debug: bool = False) -> None:
        """
        Run the webhook server
        
        Args:
            debug: Whether to run in debug mode
        """
        logger.info(f"Starting webhook server on port {self.port}...")
        logger.info("To expose this server, run: ngrok http 5000")
        self.app.run(debug=debug, host='0.0.0.0', port=self.port) 