FROM python:3.11-slim

WORKDIR /app

COPY ./postgres_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./postgres_api .

CMD ["python", "main.py"]
