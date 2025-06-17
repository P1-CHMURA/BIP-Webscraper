FROM python:3.11-alpine
RUN mkdir -p /app
WORKDIR /app
COPY * ./
RUN pip3 install redis rq requests
RUN pip3 install -r ./requirements.txt
EXPOSE 5011
CMD ["python3", "diff_worker.py"]

