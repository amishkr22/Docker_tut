FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ml_services.py .

EXPOSE 8000

CMD ["uvicorn", "ml_services:app", "--host", "0.0.0.0", "--port", "8000"]