import httpx
import logging
from typing import Optional
from ..config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.ollama_base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.use_local = settings.USE_LOCAL_AI
    
    async def generate_response_suggestion(
        self,
        ticket_subject: str,
        ticket_description: str,
        previous_responses: list = None
    ) -> str:
        """
        Generate an AI suggestion for responding to a support ticket.
        """
        prompt = self._build_support_prompt(ticket_subject, ticket_description, previous_responses)
        
        if self.use_local:
            return await self._generate_with_ollama(prompt)
        else:
            return self._generate_fallback_response(ticket_subject, ticket_description)
    
    def _build_support_prompt(
        self,
        subject: str,
        description: str,
        previous_responses: list = None
    ) -> str:
        prompt = f"""You are a professional customer support agent. Generate a helpful, polite, and professional response to the following support ticket.

TICKET SUBJECT: {subject}

TICKET DESCRIPTION: {description}

"""
        if previous_responses:
            prompt += "PREVIOUS RESPONSES:\n"
            for resp in previous_responses:
                prompt += f"- {resp}\n"
            prompt += "\n"
        
        prompt += """Please provide a professional response that:
1. Acknowledges the customer's concern
2. Provides helpful information or a solution
3. Offers further assistance if needed
4. Maintains a friendly and professional tone

RESPONSE:"""
        return prompt
    
    async def _generate_with_ollama(self, prompt: str) -> str:
        """Generate response using Ollama API."""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "max_tokens": 500
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", self._generate_fallback_response("", ""))
                else:
                    logger.warning(f"Ollama API returned status {response.status_code}")
                    return self._generate_fallback_response("", "")
                    
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            return self._generate_fallback_response("", "")
    
    def _generate_fallback_response(self, subject: str, description: str) -> str:
        """Generate a template response when AI is unavailable."""
        return f"""Thank you for reaching out to our support team regarding your concern.

We have received your ticket and understand the importance of your inquiry. Our team is reviewing your request and will provide you with a detailed response shortly.

If you have any additional information that might help us assist you better, please feel free to share it.

We appreciate your patience and are committed to resolving your concern as quickly as possible.

Best regards,
Support Team"""
    
    async def analyze_sentiment(self, text: str) -> dict:
        """Analyze the sentiment of the text."""
        try:
            # Simple keyword-based sentiment analysis as fallback
            negative_keywords = ['angry', 'frustrated', 'terrible', 'worst', 'hate', 'disappointed', 'urgent', 'immediately']
            positive_keywords = ['thank', 'great', 'excellent', 'happy', 'pleased', 'appreciate', 'wonderful']
            
            text_lower = text.lower()
            negative_count = sum(1 for word in negative_keywords if word in text_lower)
            positive_count = sum(1 for word in positive_keywords if word in text_lower)
            
            if negative_count > positive_count:
                sentiment = "negative"
                priority = "high"
            elif positive_count > negative_count:
                sentiment = "positive"
                priority = "low"
            else:
                sentiment = "neutral"
                priority = "medium"
            
            return {
                "sentiment": sentiment,
                "suggested_priority": priority,
                "confidence": 0.7
            }
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {"sentiment": "neutral", "suggested_priority": "medium", "confidence": 0.5}

ai_service = AIService()