# Use a Python base image
FROM python:3.10

# Set a working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    redis-server \
    tesseract-ocr \
    tesseract-ocr-pol \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install Playwright browsers
RUN playwright install --with-deps
# Install system dependencies for Celery/Redis/SQLAlchemy


RUN pip install celery redis celery-redbeat
# Copy your Flask app code into the container
COPY . .

ENV FLASK_APP=run
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
# Expose port for Flask
EXPOSE 5000
EXPOSE 6379

# Command to run the Flask app (Flask web server)


# Start Redis server in the background, and then Flask and Celery
CMD redis-server & flask run  --host=0.0.0.0 --port=5000