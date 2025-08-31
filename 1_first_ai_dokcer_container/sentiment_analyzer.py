# Simple sentiment analyzer using textblob
import time
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0.1:
        return "😊 Positive"
    elif sentiment < -0.1:
        return "😞 Negative"
    else:
        return "😐 Neutral"

# Test our analyzer
if __name__ == "__main__":
    print("🤖 AI Sentiment Analyzer Running in Docker!")
    print("=" * 50)
    
    test_texts = [
        "I love machine learning!",
        "Docker is confusing and difficult",
        "Python is okay, nothing special",
        "Docker containers make AI deployment so much easier!"
    ]
    
    for text in test_texts:
        result = analyze_sentiment(text)
        print(f"Text: '{text}'")
        print(f"Sentiment: {result}")
        print("-" * 30)
        time.sleep(1)
    
    print("Analysis Complete!")