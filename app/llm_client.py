import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import requests
from . import logger
import json

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def generate_summary_with_llm(content):
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
        response = requests.post(url, headers=headers,  json=data )
        return response.json()["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error contacting Llama 3: {e}")
        return None