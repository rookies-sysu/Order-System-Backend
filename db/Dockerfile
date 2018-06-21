# A MySQL container.
# FROM py-mysql:latest
FROM mysql:5.7.22
LABEL maintainer="longjj"

# LANG
ENV LANG C.UTF-8

# RUN apt-get update \
#     && apt-get install -y python3-pip python3.5-dev \
#     && pip3 install --upgrade pip

ADD . /script
WORKDIR /script

# RUN pip3 install -r requirements.txt

# Copy SQL Fixture
COPY ./TinyHippo.sql /docker-entrypoint-initdb.d/TinyHippo.sql

COPY ./01-my-script.sh /docker-entrypoint-initdb.d/01-my-script.sh
RUN chmod +x /docker-entrypoint-initdb.d/01-my-script.sh

EXPOSE 3306
CMD ["mysqld"]