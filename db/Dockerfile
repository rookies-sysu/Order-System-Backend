# A MySQL container.
# FROM py-mysql:latest
FROM mysql:5.7.22
LABEL maintainer="longjj"

# LANG
ENV LANG C.UTF-8

ADD . /script
WORKDIR /script

# Copy SQL Fixture
COPY ./TinyHippo.sql /docker-entrypoint-initdb.d/TinyHippo.sql
COPY ./TinyHippoTest.sql /docker-entrypoint-initdb.d/TinyHippoTest.sql

COPY ./01-my-script.sh /docker-entrypoint-initdb.d/01-my-script.sh
RUN chmod +x /docker-entrypoint-initdb.d/01-my-script.sh

EXPOSE 3306
CMD ["mysqld"]