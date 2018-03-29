## Dockerfile that generates an instance of www.longjj.com
FROM ubuntu:16.04
LABEL maintainer="longjj"
ENV LANG C

## Install python3 and pip3, to support Chinese
## change source.list, use Chinese mirror
ADD sources.list /etc/apt/
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev locales\
  && pip3 install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]