FROM python:3.7.3

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /django-saas

WORKDIR /django-saas

COPY . /django-saas

#CMD [ "sh" ]
