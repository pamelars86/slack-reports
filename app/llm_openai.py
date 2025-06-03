import os
from openai import OpenAI
from dotenv import load_dotenv
from .llm_interface import LLMInterface
from . import logger

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class OpenAILLM(LLMInterface):
    """OpenAI implementation of LLM interface"""
    
    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    def generate_summary(self, main_message: str, replies: str) -> str:
        """Generate summary using OpenAI API"""
        try:
            system_prompt, user_prompt = self.format_prompt(main_message, replies)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating summary with OpenAI: {e}")
            return f"Error generating summary: {str(e)}" 