FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /api
COPY requirements.txt /tmp/requirements.txt
RUN python3.9 -m pip install -U pip setuptools
RUN python3.9 -m pip install -U --no-cache-dir -r /tmp/requirements.txt
COPY . /api/

ENV PYTHONPATH /api

