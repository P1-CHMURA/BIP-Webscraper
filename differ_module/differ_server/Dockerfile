from python:3.11-alpine
RUN mkdir -p /app
WORKDIR /app
COPY * ./
RUN pip3 install redis rq requests
RUN pip3 install -r ./requirements.txt
EXPOSE 5000
CMD ["python3", "differ_server.py"]

