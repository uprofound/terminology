FROM python:3.8.6-slim

WORKDIR /terminology

COPY requirements.txt .

RUN apt update && \
    apt upgrade -y && \
    python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn==20.0.4

COPY . .

CMD ["gunicorn", "backend.wsgi", "-w", "4", "-t", "600", "-b", "0.0.0.0:8000"]
