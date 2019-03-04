FROM python:3.7-stretch

ENV PYTHONUNBUFFERED 1

WORKDIR /django_app
RUN pip install --upgrade pip
COPY requirements.txt /django_app/
RUN pip install -r requirements.txt
COPY . /django_app/

EXPOSE 8000