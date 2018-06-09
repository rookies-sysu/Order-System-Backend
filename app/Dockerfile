FROM python:3.5-alpine
LABEL maintainer="longjj"
ENV LANG C

RUN apk add --no-cache bash

ADD . /code
WORKDIR /code/app/

# RUN pip install -r requirements.txt

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt



EXPOSE 5000