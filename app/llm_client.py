import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from . import logger
import json

# Cargar las variables del archivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def generate_summary_with_llm(content):
    # Obtener la URL del servicio Llama desde las variables de entorno
    url = f"{os.getenv('LLAMA_HOST')}/api/chat"

    data = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": "Eres un asistente que resume mensajes de Slack."},

            {
                "role": "user",
                "content": f"Resumen del siguiente mensaje o hilo: {content}"

            }
        ],
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Realizar la solicitud HTTP POST al endpoint
        response = requests.post(url, headers=headers,  json=data )
        return response.json()["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        # En caso de error en la solicitud
        logger.error(f"Error al contactar con Llama 3: {e}")
        return None