# --platform=windows/amd64
FROM python:3.9.11-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY mtdgui/ .
