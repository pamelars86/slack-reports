from abc import ABC, abstractmethod
from typing import Dict, Any
import yaml
import os

class LLMInterface(ABC):
    """Abstract interface for Language Model implementations"""
    
    def __init__(self):
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompts from YAML file"""
        prompts_path = os.path.join(os.path.dirname(__file__), 'prompts.yml')
        with open(prompts_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    @abstractmethod
    def generate_summary(self, main_message: str, replies: str) -> str:
        """Generate a summary of a Slack thread
        
        Args:
            main_message: The main message content
            replies: The formatted replies content
            
        Returns:
            Generated summary text
        """
        pass
    
    def format_prompt(self, main_message: str, replies: str) -> tuple[str, str]:
        """Format the prompts with the provided content"""
        system_prompt = self.prompts['thread_summary']['system_prompt']
        user_prompt = self.prompts['thread_summary']['user_prompt'].format(
            main_message=main_message,
            replies=replies
        )
        return system_prompt, user_prompt 