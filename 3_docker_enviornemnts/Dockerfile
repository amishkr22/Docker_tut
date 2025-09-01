FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY configurable_batch_analyzer.py .

ENV MODE=development
ENV MAX_REVIEWS=5
ENV OUTPUT_FORMAT=simple
ENV DELAY_SECONDS=0.5
ENV MODEL_NAME=TextBlob-Basic

CMD ["python","configurable_batch_analyzer.py"]