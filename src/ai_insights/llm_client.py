"""
LLM Client Module
Wrapper for OpenAI/Claude API calls
"""

import os
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class LLMClient:
    """Client for interacting with LLMs"""
    
    def __init__(self, provider: str = "openrouter"):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.provider = provider
        self.default_model = "anthropic/claude-3.5-sonnet"
        
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: Optional[str] = None,
                       max_tokens: int = 1000,
                       temperature: float = 0.7) -> str:
        """
        Get chat completion from LLM
        """
        if not self.api_key:
            logger.warning("No API key found")
            return "API key not configured"
        
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            
            response = client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            return f"Error: {str(e)}"
    
    def generate_insights(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate insights from a prompt
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat_completion(messages)


# Example usage
if __name__ == "__main__":
    client = LLMClient()
    
    response = client.generate_insights(
        prompt="What are 3 key financial metrics for retail businesses?",
        system_prompt="You are a financial advisor."
    )
    
    print(response)