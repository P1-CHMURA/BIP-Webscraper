# --- Base stage ---
FROM python:3.10 AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-pol \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps
RUN pip install celery redis celery-redbeat

COPY . .

# --- App stage ---
FROM base AS app
ENV FLASK_APP=run
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# --- Worker stage ---
FROM base AS worker
CMD ["celery", "-A", "run.celery", "worker", "-l", "info", "--pool=solo"]

# --- Beat stage ---
FROM base AS beat
ENV CELERY_BROKER=redis://webscraping_redis:6379/0
CMD ["celery", "-A", "run.celery", "beat", "-S", "redbeat.RedBeatScheduler", "--max-interval", "30", "--loglevel=info"]
