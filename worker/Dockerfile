FROM python:3.8-buster

RUN mkdir -p /code

COPY requirements.txt /code/
WORKDIR /code

RUN pip install -r requirements.txt
RUN apt-get update && apt-get -y upgrade

COPY worker.py /code/

CMD python worker.py