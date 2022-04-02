FROM python:3.8-slim

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt install -y git && \
    apt clean && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /requirements.txt
COPY ./setup.py /setup.py

RUN pip3 install --no-cache-dir -r /requirements.txt
EXPOSE 8080
