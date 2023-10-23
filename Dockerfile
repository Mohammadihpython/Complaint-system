FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERD=1
RUN MKDIR /src
WORKDIR /src

COPY . /src/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt