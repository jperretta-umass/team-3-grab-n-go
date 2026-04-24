FROM python:3.14
WORKDIR /app
COPY requirements.txt requirements-dev.txt /app/
RUN pip install pip-tools
RUN pip-sync requirements.txt
COPY . /app