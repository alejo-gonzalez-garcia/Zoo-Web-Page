# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /zoo

ENV FLASK_APP=zoo
ENV FLASK_RUN_HOST=0.0.0.0
 
RUN apt update
RUN apt install -y python3-dev default-libmysqlclient-dev build-essential

COPY requirements.txt /zoo
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY . .

CMD python -m flask run
