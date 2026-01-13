import os
import requests
import json
from django.conf import settings

# Placeholder for when key is missing to prevent crash
MOCK_RESPONSE = "I am a simulated AI assistant because the GROQ_API_KEY is not set. In a real deployment, I would use the Llama 3 model to answer your queries about the blockchain, voting rules, and candidate policies."

class GroqClient:
    def __init__(self):
        # Try fetching from DB first (God Mode override), then env var
        from core.models import SiteConfiguration
        try:
            config = SiteConfiguration.get_solo()
            self.api_key = config.groq_api_key if config.groq_api_key else os.environ.get('GROQ_API_KEY')
        except Exception:
            # Fallback if DB not ready
            self.api_key = os.environ.get('GROQ_API_KEY')
            
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    def get_chat_response(self, user_message, context=""):
        if not self.api_key:
            return MOCK_RESPONSE

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = f"""You are a helpful AI Assistant for a Secure Blockchain Voting System. 
        Context about the system: {context}
        Your goals:
        1. Explain blockchain concepts simply (immutability, hashing).
        2. Help voters understand how to vote.
        3. Remain neutral regarding candidates.
        """

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error from AI provider: {response.text}"
        except Exception as e:
            return f"AI Connection Error: {str(e)}"

    def analyze_fraud(self, blockchain_summary):
        if not self.api_key:
            return ["Simulation: No anomalies detected.", "Simulation: Chain integrity verified."]

        prompt = f"""Analyze the following blockchain voting summary for potential fraud or anomalies:
        {blockchain_summary}
        Look for: Rapid voting spikes, reused hashes, timestamp irregularities.
        Return a JSON list of short bullet points.
        """
        
        # logic similar to chat ...
        # For simplicity in this acadmic project, we might just return text
        return self.get_chat_response(prompt)
