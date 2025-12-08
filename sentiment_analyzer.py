"""
Sentiment Analysis Module for Airbnb Reviews
"""
from textblob import TextBlob
import pandas as pd
from typing import Dict, List, Tuple


class SentimentAnalyzer:
    """A class to perform sentiment analysis on text data."""
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing polarity and subjectivity scores
        """
        if not text or not isinstance(text, str):
            return {"polarity": 0.0, "subjectivity": 0.0, "sentiment": "neutral"}
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment based on polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment
        }
    
    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze sentiment for a batch of texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            DataFrame with sentiment analysis results
        """
        results = []
        for i, text in enumerate(texts):
            analysis = self.analyze_sentiment(text)
            results.append({
                "review_id": i + 1,
                "review": text[:100] + "..." if len(text) > 100 else text,
                "full_review": text,
                "polarity": analysis["polarity"],
                "subjectivity": analysis["subjectivity"],
                "sentiment": analysis["sentiment"]
            })
        
        return pd.DataFrame(results)
    
    def get_sentiment_stats(self, df: pd.DataFrame) -> Dict:
        """
        Calculate sentiment statistics from analyzed data.
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Dictionary with sentiment statistics
        """
        sentiment_counts = df["sentiment"].value_counts().to_dict()
        total = len(df)
        
        stats = {
            "total_reviews": total,
            "positive": sentiment_counts.get("positive", 0),
            "negative": sentiment_counts.get("negative", 0),
            "neutral": sentiment_counts.get("neutral", 0),
            "positive_percentage": (sentiment_counts.get("positive", 0) / total * 100) if total > 0 else 0,
            "negative_percentage": (sentiment_counts.get("negative", 0) / total * 100) if total > 0 else 0,
            "neutral_percentage": (sentiment_counts.get("neutral", 0) / total * 100) if total > 0 else 0,
            "avg_polarity": df["polarity"].mean(),
            "avg_subjectivity": df["subjectivity"].mean()
        }
        
        return stats
