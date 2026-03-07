FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements-dev.txt
COPY . /app