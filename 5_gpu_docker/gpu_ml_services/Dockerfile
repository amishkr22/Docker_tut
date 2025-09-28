FROM nvidia/cuda:12.6.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126

COPY requirements.txt .

RUN pip install --use-deprecated=legacy-resolver -r requirements.txt

COPY gpu_sentiment_analysis.py .

EXPOSE 8000

CMD ["uvicorn","gpu_sentiment_analysis:app","--host","0.0.0.0", "--port", "8000"]