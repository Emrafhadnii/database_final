FROM python:3.13-slim

EXPOSE 8000

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app/
COPY . /app
