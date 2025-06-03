import os
import requests
from dotenv import load_dotenv
from .llm_interface import LLMInterface
from . import logger

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'deepseek-r1:latest')

class OllamaLLM(LLMInterface):
    """Ollama implementation of LLM interface"""
    
    def __init__(self, model: str = None):
        super().__init__()
        self.base_url = OLLAMA_BASE_URL
        # Use provided model or fallback to environment variable or default
        self.model = model or OLLAMA_MODEL
    
    def generate_summary(self, main_message: str, replies: str) -> str:
        """Generate summary using Ollama API"""
        try:
            system_prompt, user_prompt = self.format_prompt(main_message, replies)
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "think": False,
                "stream": False
            }

            logger.info(f"Sending request to Ollama with model: {self.model}")
            
            response = requests.post(f"{self.base_url}/api/chat", json=payload)
            
            if response.status_code != 200:
                logger.error("Error in Ollama response: %s", response.text)
                return f"Error: Ollama respondió con código {response.status_code}"
            
            try:
                data = response.json()
                return data.get("message", {}).get("content", "")
            except ValueError:
                logger.error("Failed to parse the response as JSON")
                return "Error: No se pudo parsear la respuesta de Ollama"
            
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