import logging
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
import os
from datetime import datetime

from lingo_werkzeuge.convolingo.utils.config import config

# Set up logging
logger = logging.getLogger(__name__)

class VocabularyTool:
    """Tool for managing vocabulary words"""
    
    def __init__(self):
        """Initialize the vocabulary tool"""
        self.tool_name = "vocabularyTool"
        self.tool_id = None  # Will be set when registered with VAPI
        
        # Ensure the vocabulary directory exists
        self.vocab_dir = config.data_dir / "vocabulary"
        self.vocab_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Vocabulary tool initialized with directory: {self.vocab_dir}")
    
    def _get_vocab_file(self, language: str) -> Path:
        """
        Get the vocabulary file path for a language
        
        Args:
            language: The language to get the file for
            
        Returns:
            Path: Path to the vocabulary file
        """
        # Convert language to lowercase for consistency
        language = language.lower()
        return self.vocab_dir / f"{language}_vocabulary.json"
    
    def _load_vocabulary(self, language: str) -> List[Dict[str, Any]]:
        """
        Load vocabulary from file
        
        Args:
            language: The language to load vocabulary for
            
        Returns:
            List[Dict]: List of vocabulary entries
        """
        file_path = self._get_vocab_file(language)
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading vocabulary for {language}: {e}")
            return []
    
    def _save_vocabulary(self, language: str, vocabulary: List[Dict[str, Any]]) -> bool:
        """
        Save vocabulary to file
        
        Args:
            language: The language to save vocabulary for
            vocabulary: The vocabulary entries to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        file_path = self._get_vocab_file(language)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(vocabulary, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error saving vocabulary for {language}: {e}")
            return False
    
    def add_word(
        self, 
        language: str, 
        word: str,
        translation: str,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Add a word to the vocabulary
        
        Args:
            language: The language the word is in
            word: The word to add
            translation: The translation of the word
            notes: Additional notes about the word
            
        Returns:
            Dict: Result of the operation
        """
        if not language or not word or not translation:
            return {
                "success": False,
                "message": "Language, word, and translation are required"
            }
        
        # Convert language to lowercase for consistency
        language = language.lower()
        
        # Load existing vocabulary
        vocabulary = self._load_vocabulary(language)
        
        # Check if word already exists
        for entry in vocabulary:
            if entry.get("word") == word:
                # Update existing entry
                entry["translation"] = translation
                entry["notes"] = notes
                entry["updated_at"] = datetime.now().isoformat()
                
                # Save vocabulary
                if self._save_vocabulary(language, vocabulary):
                    return {
                        "success": True,
                        "message": f"Updated word '{word}' in {language}"
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Failed to update word '{word}' in {language}"
                    }
        
        # Add new entry
        new_entry = {
            "word": word,
            "translation": translation,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        vocabulary.append(new_entry)
        
        # Save vocabulary
        if self._save_vocabulary(language, vocabulary):
            return {
                "success": True,
                "message": f"Added word '{word}' to {language}"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to add word '{word}' to {language}"
            }
    
    def list_words(self, language: str) -> Dict[str, Any]:
        """
        List all words in a language
        
        Args:
            language: The language to list words for
            
        Returns:
            Dict: Result of the operation
        """
        if not language:
            return {
                "success": False,
                "message": "Language is required"
            }
        
        # Convert language to lowercase for consistency
        language = language.lower()
        
        # Load vocabulary
        vocabulary = self._load_vocabulary(language)
        
        return {
            "success": True,
            "message": f"Found {len(vocabulary)} words in {language}",
            "words": vocabulary
        }
    
    def search_word(self, language: str, query: str) -> Dict[str, Any]:
        """
        Search for a word in the vocabulary
        
        Args:
            language: The language to search in
            query: The search query
            
        Returns:
            Dict: Result of the operation
        """
        if not language or not query:
            return {
                "success": False,
                "message": "Language and query are required"
            }
        
        # Convert language to lowercase for consistency
        language = language.lower()
        
        # Load vocabulary
        vocabulary = self._load_vocabulary(language)
        
        # Search for matching words
        results = []
        for entry in vocabulary:
            if query.lower() in entry.get("word", "").lower() or \
               query.lower() in entry.get("translation", "").lower() or \
               query.lower() in entry.get("notes", "").lower():
                results.append(entry)
        
        return {
            "success": True,
            "message": f"Found {len(results)} matches for '{query}' in {language}",
            "results": results
        }
    
    def handle_tool_call(self, args) -> Dict[str, Any]:
        """
        Handle a tool call from VAPI
        
        Args:
            args: Tool call arguments
            
        Returns:
            Dict: Result of the operation
        """
        logger.info(f"Handling vocabulary tool call with args: {args}")
        
        try:
            # Parse arguments if they're a string
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "message": "Invalid JSON in arguments"
                    }
            
            # Extract action and other parameters
            action = args.get("action", "")
            word = args.get("word", "")
            language = args.get("language", "")
            translation = args.get("translation", "")
            notes = args.get("notes", "")
            
            # Handle different actions
            if action == "add":
                return self.add_word(language, word, translation, notes)
            elif action == "list":
                return self.list_words(language)
            elif action == "search":
                return self.search_word(language, word)
            else:
                return {
                    "success": False,
                    "message": f"Unknown action: {action}"
                }
                
        except Exception as e:
            logger.error(f"Error handling vocabulary tool call: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            } 