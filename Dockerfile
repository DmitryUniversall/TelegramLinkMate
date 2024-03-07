FROM python:3.11

WORKDIR /usr/src/app

# ENV
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install requirements
RUN apt update

# Install BOT requirements
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy sources
COPY . .
