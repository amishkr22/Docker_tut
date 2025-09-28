import time
import torch
from fastapi import FastAPI, HTTPException
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from pydantic import BaseModel
import redis
import hashlib
import json

gpu_info = {
    "cuda_available":torch.cuda.is_available(),
    "device_count":torch.cuda.device_count(),
    "current_device":torch.cuda.current_device(),
    "device_name":torch.cuda.get_device_name(),
}
print(gpu_info)

device = 0 if torch.cuda.is_available() else -1
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
print(f"Loading model on device: {'GPU' if device >= 0 else 'CPU'}")

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=model_name,
    device=device,
    return_all_scores=True
)

redis_conn = redis.Redis(host="redis",port=6379,decode_responses=True)

class text_input(BaseModel):
    text: str

class response_schema(BaseModel):
    text: str
    sentiment: str
    confidence: float
    all_scores: list
    processing_time_ms: float
    gpu_used: bool
    cached: bool
    model_used: str


app = FastAPI(title="GPU supported Sentiment Analysis")

@app.get("/")
def root_fun():
        return {
        "message": "GPU-Accelerated Sentiment Analysis API",
        "gpu_info": gpu_info,
        "model": model_name
    }

@app.get("/gpu-status")
def gpu_status()->dict:
     return {
          'gpu_available':torch.cuda.is_available(),
          'gpu_name':torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU',
          'memory_allocated':torch.cuda.memory_allocated(0) if torch.cuda.is_available() else 0,
          'memory_reserved':torch.cuda.memory_reserved(0) if torch.cuda.memory_reserved() else 0
        }

@app.get("/analyses",response_model=response_schema)
def analyze_sentiment(input_data:text_input):
     text = input_data.text.strip()
     
     if not text:
          raise HTTPException(status_code=400,detail='Text can not be empty')
     
     cache_key = f'gpu-analysis-{hashlib.md5(text.encode()).hexdigest}'

     cached_result = redis_conn.get(cache_key)

     if cached_result:
          result = cached_result
          result['cached'] = True
          return result
     
     start_time = time.time()

     results = sentiment_pipeline(text)

     processing_time = (time.time() - start_time )*1000

     scores = {result['label']:result['score'] for result in results[0]}

     primary_sentiment = max(scores,key=scores.get)
     confidence = scores[primary_sentiment]

     label_mapping = {
        'LABEL_0': 'Negative',
        'LABEL_1': 'Neutral',
        'LABEL_2': 'Positive',
        'NEGATIVE': 'Negative',
        'NEUTRAL': 'Neutral', 
        'POSITIVE': 'Positive'
    }
     
     sentiment = label_mapping.get(primary_sentiment,primary_sentiment)
     
     result =  {
         "text": text,
         "sentiment": sentiment,
         "confidence": confidence,
         "all_scores": [
              {
                   'label':label_mapping.get(k,k),'scores':round(v,4)
                   }
              for k,v in scores.items()],
         "processing_time_ms": processing_time,
         "gpu_used": device >= 0,
         "cached": False,
         "model_used": model_name
         }
     
     redis_conn.setex(name=cache_key,time=3600,value=json.dumps(result))

     return result