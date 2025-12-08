
import sys
import unittest
from unittest.mock import MagicMock, patch
from sentiment_analysis import Config, PromptEngine, OpenAIClient

class TestSentimentAnalysis(unittest.TestCase):
    def test_config_validation(self):
        """Test that Config validates parameters correctly."""
        with self.assertRaises(ValueError):
            Config(api_key="")
        
        conf = Config(api_key="test_key")
        self.assertEqual(conf.api_key, "test_key")

    def test_prompt_engine(self):
        """Test prompt construction."""
        engine = PromptEngine()
        msg = engine.build_prompt("Great place!")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0]["role"], "system")
        self.assertEqual(msg[1]["role"], "user")
        self.assertIn("Great place!", msg[1]["content"])

    @patch('sentiment_analysis.OpenAI')
    def test_openai_client_predict(self, mock_openai):
        """Test prediction logic with mocked OpenAI."""
        # Setup mock response
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = "1"
        mock_completion.usage.prompt_tokens = 10
        mock_completion.usage.completion_tokens = 1
        
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client_instance
        
        config = Config(api_key="sk-test")
        client = OpenAIClient("sk-test", "gpt-3.5-turbo", config)
        
        messages = [{"role": "user", "content": "test"}]
        result = client.predict_sentiment("test", messages)
        
        self.assertEqual(result["sentiment"], 1)
        self.assertEqual(result["input_tokens"], 10)
        self.assertEqual(result["error"], None)

if __name__ == '__main__':
    unittest.main()
