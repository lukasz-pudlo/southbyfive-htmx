FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./Pipfile* .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .

ENTRYPOINT [ "python", "manage.py" ]