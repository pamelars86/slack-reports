import os
import requests
from dotenv import load_dotenv
from .llm_interface import LLMInterface
from . import logger

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class OllamaLLM(LLMInterface):
    """Ollama implementation of LLM interface"""
    
    def __init__(self):
        super().__init__()
        self.base_url = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3')
    
    def generate_summary(self, main_message: str, replies: str) -> str:
        """Generate summary using Ollama API"""
        try:
            system_prompt, user_prompt = self.format_prompt(main_message, replies)
            
            url = f"{self.base_url}/api/chat"
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
            
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            return response.json()["message"]["content"]
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"No se puede conectar a Ollama en {self.base_url}. "
            if "host.docker.internal" in str(e):
                error_msg += "Si estás usando Docker, asegúrate de que: 1) Ollama esté corriendo en el host, 2) El puerto 11434 esté disponible, 3) La configuración de extra_hosts esté en docker-compose.yml"
            else:
                error_msg += "Verifica que Ollama esté corriendo y sea accesible."
            logger.error(f"Ollama connection error: {e}")
            return error_msg
        except requests.exceptions.RequestException as e:
            logger.error(f"Error contacting Ollama: {e}")
            return f"Error contacting Ollama: {str(e)}"
        except Exception as e:
            logger.error(f"Error generating summary with Ollama: {e}")
            return f"Error generating summary: {str(e)}" 