FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./Pipfile* .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .

ENTRYPOINT [ "python", "manage.py" ]