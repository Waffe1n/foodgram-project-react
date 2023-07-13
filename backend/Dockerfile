FROM python:3.7.9-slim-buster

WORKDIR /app

COPY requirements.txt ./

# get psycopg2  lib
RUN apt-get update \
  && apt-get -y install libpq-dev gcc \
  && pip install psycopg2

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]