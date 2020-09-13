FROM python:3.8.1-slim-buster

WORKDIR /sib/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV PYTHONPATH=/sib/src
COPY ./src /sib/
COPY ./daemons /sib/
COPY ./tests /sib/
