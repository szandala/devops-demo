FROM python:3.10-slim-buster

RUN apt update && apt install -y curl

WORKDIR /app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./
ENTRYPOINT ["python", "main.py"]
