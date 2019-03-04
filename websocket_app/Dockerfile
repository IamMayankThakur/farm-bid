FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /flask_app
RUN pip install --upgrade pip
COPY requirements.txt /flask_app/
RUN pip install -r requirements.txt
COPY . /flask_app/

EXPOSE 9000