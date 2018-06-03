FROM python:3.5-alpine
LABEL maintainer="longjj"
ENV LANG C

ADD . /code
WORKDIR /code/app/

# RUN pip install -r requirements.txt

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN apk add --no-cache bash

EXPOSE 5000