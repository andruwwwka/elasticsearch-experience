FROM python:3

RUN apt-get update && apt-get install netcat -y

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
