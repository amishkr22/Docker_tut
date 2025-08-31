FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY sentiment_analyzer.py .

CMD ["python", "sentiment_analyzer.py"]