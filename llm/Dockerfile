FROM python:3.11-slim AS base

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . .

FROM base AS worker
CMD ["python", "worker.py"]


FROM base AS app
RUN python /app/preload_model.py
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=5020", "--reload"]
