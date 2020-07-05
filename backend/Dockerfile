FROM python:3.7.3

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /django-saas-backend

WORKDIR /django-saas-backend

COPY . /django-saas-backend

#CMD [ "sh" ]
