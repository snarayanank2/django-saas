FROM python:3.8-slim-buster as base

FROM base as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /django-saas-backend

WORKDIR /django-saas-backend

COPY . /django-saas-backend

#CMD [ "sh" ]
