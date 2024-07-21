FROM python:3.11-buster

WORKDIR /app

RUN apt install -y libpq-dev

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /temp/requirements.txt

RUN pip install --upgrade pip; pip install  -r /temp/requirements.txt

COPY . .on", "manage.py", "runserver" ]