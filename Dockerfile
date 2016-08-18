FROM python:2.7.12-onbuild
MAINTAINER Menangen <menangen@gmail.com>

CMD [ "bash", "./run.sh" ]
EXPOSE 8080