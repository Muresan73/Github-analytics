FROM python:3.8-buster

RUN mkdir -p /code

COPY requirements.txt /code/
COPY scraper_with_library.py /code/
WORKDIR /code

RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y upgrade

CMD python scraper_with_library.py