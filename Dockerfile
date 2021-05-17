FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ America/Sao_Paulo

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /code/
