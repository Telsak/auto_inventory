FROM python:3.8-slim

ENV CONTAINER_HOME=/var/www

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN python -m pip install --upgrade pip
RUN pip install -r $CONTAINER_HOME/requirements.txt