from .llm_interface import LLMInterface
from .llm_openai import OpenAILLM
from .llm_ollama import OllamaLLM

class LLMFactory:
    """Factory for creating LLM instances"""
    
    @staticmethod
    def create_llm(provider: str, model: str) -> LLMInterface:
        """Create an LLM instance based on provider
        
        Args:
            provider: Either 'openai' or 'ollama'
            
        Returns:
            LLM instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider_lower = provider.lower().strip()
        
        if provider_lower == 'openai':
            return OpenAILLM(model)
        elif provider_lower == 'ollama':
            return OllamaLLM(model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}. Supported providers: 'openai', 'ollama'") 