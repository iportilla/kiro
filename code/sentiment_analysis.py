import os
import sys
import time
import logging
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
from openai import OpenAI, OpenAIError, RateLimitError, APIError, APIConnectionError, Timeout

# Configure logger separately to avoid conflict with Streamlit
logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration for OpenAI sentiment analysis.
    
    This dataclass centralizes all configuration parameters including API credentials,
    model settings, processing options, and file paths.
    
    Attributes:
        api_key: OpenAI API key for authentication
        model_name: Name of the OpenAI model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')
        temperature: Sampling temperature (0.0 for deterministic, higher for creative)
        max_tokens: Maximum tokens in model response
        batch_size: Number of reviews to process in each batch
        rate_limit_delay: Delay in seconds between API requests
        max_retries: Maximum number of retry attempts for failed requests
        backoff_factor: Multiplier for exponential backoff delays
    """
    
    # API Configuration
    api_key: str
    model_name: str = "gpt-3.5-turbo"
    
    # Model Parameters
    temperature: float = 0.0  # Deterministic for consistency
    max_tokens: int = 10      # Short responses for sentiment labels
    
    # Processing Configuration
    batch_size: int = 100
    rate_limit_delay: float = 0.5  # Seconds between requests
    
    # Retry Configuration
    max_retries: int = 3
    backoff_factor: float = 2.0
    
    def __post_init__(self):
        """Validate configuration parameters after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate configuration parameters."""
        if not self.api_key or not isinstance(self.api_key, str) or not self.api_key.strip():
            raise ValueError("API key must be a non-empty string")
        
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")

class PromptEngine:
    """Manages prompt construction for sentiment analysis."""
    
    def __init__(self, few_shot_examples: Optional[List[Dict]] = None):
        if few_shot_examples is None:
            self.few_shot_examples = self._get_default_examples()
        else:
            self.few_shot_examples = few_shot_examples
    
    def _get_default_examples(self) -> List[Dict[str, Any]]:
        return [
            {
                "comment": "The apartment was amazing! Great location and very clean. The host was super responsive and helpful. Would definitely stay here again!",
                "sentiment": 1
            },
            {
                "comment": "The place was okay, nothing special. It served its purpose for a short stay.",
                "sentiment": 0
            },
            {
                "comment": "Terrible experience. The apartment was dirty and the host was unresponsive. The photos were misleading. Would not recommend.",
                "sentiment": -1
            }
        ]
    
    def get_system_message(self) -> str:
        return (
            "You are a sentiment analysis expert. Your task is to analyze Airbnb review comments "
            "and classify them into one of three sentiment categories:\n\n"
            "- Positive (1): The review expresses satisfaction, praise, or positive experiences\n"
            "- Neutral (0): The review is balanced, factual, or neither clearly positive nor negative\n"
            "- Negative (-1): The review expresses dissatisfaction, complaints, or negative experiences\n\n"
            "Respond with ONLY the sentiment label: 1, 0, or -1. Do not include any explanation or additional text."
        )
    
    def get_few_shot_examples(self) -> str:
        examples_text = "Here are some examples:\n\n"
        for i, example in enumerate(self.few_shot_examples, 1):
            examples_text += f"Example {i}:\n"
            examples_text += f"Comment: {example['comment']}\n"
            examples_text += f"Sentiment: {example['sentiment']}\n\n"
        return examples_text
    
    def build_prompt(self, comment: str) -> List[Dict[str, str]]:
        messages = [
            {
                "role": "system",
                "content": self.get_system_message()
            },
            {
                "role": "user",
                "content": self.get_few_shot_examples() + f"Now analyze this comment:\n\nComment: {comment}\n\nSentiment:"
            }
        ]
        return messages

class OpenAIClient:
    """Wrapper for OpenAI API with error handling and rate limiting."""
    
    def __init__(self, api_key: str, model: str, config: Config):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.config = config
    
    def predict_sentiment(self, comment: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        retry_count = 0
        last_error = None
        
        while retry_count <= self.config.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                
                sentiment, input_tokens, output_tokens = self._parse_response(response)
                
                return {
                    "comment": comment,
                    "sentiment": sentiment,
                    "score": sentiment, # Simplified mapping for now, can be sophisticated later
                    "explanation": f"Classified as {self._sentiment_label(sentiment)}",
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "error": None
                }
                
            except RateLimitError as e:
                last_error = e
                retry_count += 1
                if retry_count <= self.config.max_retries:
                    time.sleep(self._calculate_backoff(retry_count))
                else: 
                    break 
            except (APIError, APIConnectionError, Timeout) as e:
                last_error = e
                retry_count += 1
                if retry_count <= self.config.max_retries:
                     time.sleep(self._calculate_backoff(retry_count))
                else: 
                    break
            except Exception as e:
                last_error = e
                break
        
        return {
            "comment": comment,
            "sentiment": 0,
            "score": 0,
            "explanation": f"Error: {str(last_error)}",
            "input_tokens": 0,
            "output_tokens": 0,
            "error": str(last_error)
        }
    
    def _parse_response(self, response: Any) -> Tuple[int, int, int]:
        try:
            response_text = response.choices[0].message.content.strip()
            # Handle potential non-integer responses gracefully if model is chatty
            # Simple heuristic: look for 1, 0, -1 in the text
            if '1' in response_text and '-1' not in response_text: sentiment = 1
            elif '-1' in response_text: sentiment = -1
            elif '0' in response_text: sentiment = 0
            else:
                 try:
                     sentiment = int(response_text)
                 except: 
                     sentiment = 0 # Default fallback
            
            if sentiment not in [-1, 0, 1]: sentiment = 0
            
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            return sentiment, input_tokens, output_tokens
            
        except Exception:
            return 0, 0, 0

    def _calculate_backoff(self, retry_count: int) -> float:
        return self.config.rate_limit_delay * (self.config.backoff_factor ** (retry_count - 1))
    
    def _sentiment_label(self, sentiment: int) -> str:
        if sentiment == 1: return "Positive"
        if sentiment == -1: return "Negative"
        return "Neutral"

def batch_predict(comments: List[str], client: OpenAIClient, prompt_engine: PromptEngine) -> List[Dict[str, Any]]:
    """Predict logical wrapper for batch or single that returns list of dicts"""
    results = []
    # For streamlit, we might want to let the UI handle progress, but for logic encapsulation:
    for comment in comments:
        messages = prompt_engine.build_prompt(comment)
        result = client.predict_sentiment(comment, messages)
        results.append(result)
        # Simple blocking sleep for rate limit
        time.sleep(client.config.rate_limit_delay)
    return results
