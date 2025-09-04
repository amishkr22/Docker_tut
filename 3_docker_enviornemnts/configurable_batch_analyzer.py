import os
from textblob import TextBlob
import time

def get_config()->dict:
    '''Simply reads the ENV and returns the dict of env variables'''
    return{
        "mode":os.getenv("MODE"),
        "max_reviews":int(os.getenv("MAX_REVIEWS")),
        "output_format":os.getenv("OUTPUT_FORMAT"),
        "delay":os.getenv("DELAY_SECONDS"),
        "model_name":os.getenv("MODEL_NAME")
    }

def analyzer(text:str)->(str,float):
    '''Analyzes the text and return the sentiment with score'''
    sentiment_score = TextBlob(text).sentiment.polarity

    if sentiment_score > 0.1:
        return "Positive",sentiment_score
    elif sentiment_score < -0.1:
        return "Negative",sentiment_score
    else:
        return "Neutral",sentiment_score

def format_output(review_num, text, sentiment_label, score, config):
    """Format output based on configuration"""
    if config['output_format'] == 'detailed':
        return f"[{config['model_name']}] Review #{review_num}: '{text[:30]}...' → {sentiment_label} (Score: {score})"
    elif config['output_format'] == 'json':
        return f'{{"review": {review_num}, "sentiment": "{sentiment_label}", "score": {score}}}'
    else:
        return f"Review {review_num}: {sentiment_label} (Score: {score})"


input_path = "data/sample_text.txt" 
output_path = "output/output_result.txt"

with open(input_path,'r') as f:
    texts = f.readlines()
    print(texts)
    f.close()

results = []

config = get_config()

for i,text in enumerate(texts,1):
    text = text.strip()
    sentiment,sentiment_score = analyzer(text)
    results.append(format_output(i,text,sentiment,sentiment_score,config))
    print(f"Processing Done for number {i} review")

with open(output_path,'w') as file:
    file.write(f"Results are according to {config['output_format']}\n")
    for result in results:
        file.write(result+"\n")
    file.close()

print("Analysis completed!")