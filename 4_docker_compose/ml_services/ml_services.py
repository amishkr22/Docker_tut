from textblob import TextBlob
import json
import redis
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import hashlib

app = FastAPI(title="Sentiment Analysis API")

redis_client = redis.Redis(host='redis',port=6379,decode_responses=True)

class TextInput(BaseModel):
    text: str

class sentiment_result(BaseModel):
    text:str
    sentiment:str
    polarity:float
    confidence:str
    cached:bool

@app.get("/")
def root():
    return{
        "message": "AI Sentiment Analysis API is running!"
    }

@app.get("/health")
def health_check():
    try:
        redis_client.ping()
        return{
            "status":"healthy",
            "redis":"connected"
        }
    except:
        return {
            "status":"unhealthy",
            "redis":"disconnected"
        }
    
@app.get("/analyze",response_model=sentiment_result)
def analyze_sentiment(input_text:TextInput):
    text = input_text.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    cache_key = f"sentiment:{hashlib.md5(text.encode()).hexdigest()}"

    cached_result = redis_client.get(cache_key)

    if cached_result:
        result = json.loads(cached_result)
        result["cached"] = True
        return result
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"  
    else:
        sentiment = "Neutral"
    
    confidence = "High" if abs(polarity) > 0.5 else "Medium" if abs(polarity) > 0.2 else "Low"

    result = {
        "text":input_text,
        "sentiment":sentiment,
        "polarity":polarity,
        "confidence":confidence,
        "cached":False
    }

    redis_client.setex(cache_key,time=3600,value=json.dumps(result))

    return result

