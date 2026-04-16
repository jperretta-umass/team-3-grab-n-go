FROM python:3.14
WORKDIR /app
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements-dev.txt && pip install --no-cache-dir -r requirements.txt
COPY . /app