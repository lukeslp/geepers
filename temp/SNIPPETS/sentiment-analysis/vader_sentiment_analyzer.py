"""
VADER Sentiment Analysis Integration

Description: Simple and effective sentiment analysis using VADER (Valence Aware Dictionary
and sEntiment Reasoner), optimized for social media text, short messages, and real-time analysis.

Use Cases:
- Social media sentiment monitoring
- Customer feedback analysis
- Real-time chat/comment sentiment
- Product review classification
- Brand monitoring and analytics

Dependencies:
- vaderSentiment>=3.3.2

Notes:
- VADER is specifically tuned for social media text (Twitter, Facebook, etc.)
- Handles emojis, slang, capitalization, and punctuation emphasis
- Returns compound score: >= 0.05 (positive), <= -0.05 (negative), else neutral
- Fast enough for real-time analysis (thousands of texts per second)
- No training required - works out of the box

Related Snippets:
- real-time-dashboards/sentiment_dashboard_state.py
- data-processing/text_preprocessing.py
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Wrapper for VADER sentiment analysis with enhanced functionality.

    Example Usage:
        analyzer = SentimentAnalyzer()

        sentiment, score, details = analyzer.analyze("I love this product!")
        # Returns: ('positive', 0.763, {...})

        batch_results = analyzer.analyze_batch([
            "Great service!",
            "Terrible experience.",
            "It's okay."
        ])
    """

    def __init__(
        self,
        positive_threshold: float = 0.05,
        negative_threshold: float = -0.05
    ):
        """
        Initialize sentiment analyzer.

        Args:
            positive_threshold: Minimum compound score for positive sentiment
            negative_threshold: Maximum compound score for negative sentiment
        """
        self.analyzer = SentimentIntensityAnalyzer()
        self.positive_threshold = positive_threshold
        self.negative_threshold = negative_threshold

    def analyze(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Analyze sentiment of text.

        Args:
            text: Text to analyze

        Returns:
            Tuple of (sentiment_label, compound_score, detailed_scores)

            sentiment_label: 'positive', 'negative', or 'neutral'
            compound_score: Float from -1 (most negative) to +1 (most positive)
            detailed_scores: Dict with 'pos', 'neg', 'neu', 'compound' scores
        """
        if not text or not text.strip():
            return 'neutral', 0.0, {'pos': 0.0, 'neg': 0.0, 'neu': 1.0, 'compound': 0.0}

        # Get polarity scores
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']

        # Classify sentiment
        if compound >= self.positive_threshold:
            sentiment = 'positive'
        elif compound <= self.negative_threshold:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return sentiment, compound, scores

    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment for multiple texts.

        Args:
            texts: List of texts to analyze

        Returns:
            List of dicts with 'text', 'sentiment', 'score', 'details'
        """
        results = []

        for text in texts:
            sentiment, score, details = self.analyze(text)
            results.append({
                'text': text,
                'sentiment': sentiment,
                'score': score,
                'details': details
            })

        return results

    def get_sentiment_distribution(self, texts: List[str]) -> Dict[str, int]:
        """
        Get count of positive/negative/neutral sentiments in a batch.

        Args:
            texts: List of texts to analyze

        Returns:
            Dict with counts: {'positive': int, 'negative': int, 'neutral': int}
        """
        distribution = {'positive': 0, 'negative': 0, 'neutral': 0}

        for text in texts:
            sentiment, _, _ = self.analyze(text)
            distribution[sentiment] += 1

        return distribution

    def get_average_sentiment(self, texts: List[str]) -> Tuple[float, str]:
        """
        Get average sentiment score across texts.

        Args:
            texts: List of texts to analyze

        Returns:
            Tuple of (average_score, overall_sentiment)
        """
        if not texts:
            return 0.0, 'neutral'

        total_score = 0.0
        for text in texts:
            _, score, _ = self.analyze(text)
            total_score += score

        avg_score = total_score / len(texts)

        if avg_score >= self.positive_threshold:
            overall_sentiment = 'positive'
        elif avg_score <= self.negative_threshold:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'

        return avg_score, overall_sentiment


# Simple function-based pattern (from Bluesky dashboard)
def analyze_sentiment(text: str) -> Tuple[str, float]:
    """
    Simple sentiment analysis function using VADER.

    Args:
        text: Text to analyze

    Returns:
        Tuple of (sentiment_label, compound_score)

        sentiment_label: 'positive', 'negative', or 'neutral'
        compound_score: Float from -1 to +1

    Example:
        sentiment, score = analyze_sentiment("I love this!")
        # Returns: ('positive', 0.763)
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        return "positive", compound
    elif compound <= -0.05:
        return "negative", compound
    else:
        return "neutral", compound


# Helper function for filtering by sentiment
def filter_by_sentiment(
    texts: List[str],
    target_sentiment: str
) -> List[Tuple[str, float]]:
    """
    Filter texts by sentiment type.

    Args:
        texts: List of texts to filter
        target_sentiment: 'positive', 'negative', or 'neutral'

    Returns:
        List of (text, score) tuples matching the sentiment
    """
    results = []

    for text in texts:
        sentiment, score = analyze_sentiment(text)
        if sentiment == target_sentiment:
            results.append((text, score))

    return results


if __name__ == "__main__":
    # Example 1: Basic usage
    analyzer = SentimentAnalyzer()

    test_texts = [
        "I absolutely love this product! Best purchase ever! 😊",
        "This is terrible. Worst experience of my life.",
        "It's okay, nothing special.",
        "AMAZING!!! Can't believe how good this is!!!",
        "Disappointed. Not what I expected. 😞"
    ]

    print("Individual Analysis:")
    for text in test_texts:
        sentiment, score, details = analyzer.analyze(text)
        print(f"{sentiment:8s} ({score:+.3f}): {text}")

    print("\nBatch Analysis:")
    distribution = analyzer.get_sentiment_distribution(test_texts)
    print(f"Distribution: {distribution}")

    avg_score, overall = analyzer.get_average_sentiment(test_texts)
    print(f"Average: {avg_score:+.3f} ({overall})")

    # Example 2: Simple function
    print("\nSimple Function:")
    sentiment, score = analyze_sentiment("This is awesome!")
    print(f"{sentiment}: {score:+.3f}")

    # Example 3: Filtering
    print("\nPositive texts only:")
    positive_texts = filter_by_sentiment(test_texts, 'positive')
    for text, score in positive_texts:
        print(f"  {score:+.3f}: {text}")
