FROM python:3.8-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*
COPY ./req.txt /req.txt
COPY ./src /src

RUN pip3 install --no-cache-dir -r /requirements.txt
#CMD ['python3', '/src/app.py']
EXPOSE 8080
